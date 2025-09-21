"""
Anomaly Detection Module for Sales Data
Detects unusual patterns in sales data using statistical methods
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class SalesAnomalyDetector:
    def __init__(self, contamination=0.1):
        """
        Initialize the anomaly detector
        
        Args:
            contamination (float): Expected proportion of anomalies in the dataset
        """
        self.contamination = contamination
        self.isolation_forest = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def prepare_features(self, df):
        """
        Prepare features for anomaly detection
        
        Args:
            df (pd.DataFrame): Sales data
            
        Returns:
            pd.DataFrame: Features for anomaly detection
        """
        features = df.copy()
        
        # Create time-based features
        features['day_of_week'] = features['ORDERDATE'].dt.dayofweek
        features['month'] = features['ORDERDATE'].dt.month
        features['quarter'] = features['ORDERDATE'].dt.quarter
        features['is_weekend'] = features['day_of_week'].isin([5, 6]).astype(int)
        
        # Create sales-based features
        features['sales_per_quantity'] = features['SALES'] / features['QUANTITYORDERED']
        features['log_sales'] = np.log1p(features['SALES'])
        
        # Create categorical encodings
        features['product_encoded'] = pd.Categorical(features['PRODUCTLINE']).codes
        features['country_encoded'] = pd.Categorical(features['COUNTRY']).codes
        features['status_encoded'] = pd.Categorical(features['STATUS']).codes
        
        # Select numerical features for anomaly detection
        feature_columns = [
            'SALES', 'QUANTITYORDERED', 'day_of_week', 'month', 'quarter',
            'is_weekend', 'sales_per_quantity', 'log_sales',
            'product_encoded', 'country_encoded', 'status_encoded'
        ]
        
        return features[feature_columns].fillna(0)
    
    def fit(self, df):
        """
        Fit the anomaly detection model
        
        Args:
            df (pd.DataFrame): Training sales data
        """
        features = self.prepare_features(df)
        features_scaled = self.scaler.fit_transform(features)
        self.isolation_forest.fit(features_scaled)
        self.is_fitted = True
        
    def predict(self, df):
        """
        Predict anomalies in the data
        
        Args:
            df (pd.DataFrame): Sales data to analyze
            
        Returns:
            pd.DataFrame: Original data with anomaly predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
            
        features = self.prepare_features(df)
        features_scaled = self.scaler.transform(features)
        
        # Get anomaly scores and predictions
        anomaly_scores = self.isolation_forest.decision_function(features_scaled)
        anomaly_predictions = self.isolation_forest.predict(features_scaled)
        
        # Create results dataframe
        results = df.copy()
        results['anomaly_score'] = anomaly_scores
        results['is_anomaly'] = anomaly_predictions == -1
        results['anomaly_severity'] = np.abs(anomaly_scores)
        
        return results
    
    def get_anomaly_summary(self, results_df):
        """
        Get summary of detected anomalies
        
        Args:
            results_df (pd.DataFrame): Results from predict method
            
        Returns:
            dict: Summary statistics of anomalies
        """
        anomalies = results_df[results_df['is_anomaly']]
        
        if len(anomalies) == 0:
            return {
                'total_anomalies': 0,
                'anomaly_rate': 0.0,
                'message': 'No anomalies detected'
            }
        
        summary = {
            'total_anomalies': len(anomalies),
            'anomaly_rate': len(anomalies) / len(results_df) * 100,
            'avg_anomaly_score': anomalies['anomaly_score'].mean(),
            'max_anomaly_score': anomalies['anomaly_score'].min(),  # More negative = more anomalous
            'anomaly_by_product': anomalies['PRODUCTLINE'].value_counts().to_dict(),
            'anomaly_by_country': anomalies['COUNTRY'].value_counts().to_dict(),
            'anomaly_by_status': anomalies['STATUS'].value_counts().to_dict(),
            'top_anomalous_orders': anomalies.nsmallest(5, 'anomaly_score')[['ORDERNUMBER', 'SALES', 'anomaly_score']].to_dict('records')
        }
        
        return summary

def detect_sales_anomalies(df, contamination=0.1):
    """
    Convenience function to detect anomalies in sales data
    
    Args:
        df (pd.DataFrame): Sales data
        contamination (float): Expected proportion of anomalies
        
    Returns:
        tuple: (results_df, summary_dict)
    """
    detector = SalesAnomalyDetector(contamination=contamination)
    detector.fit(df)
    results = detector.predict(df)
    summary = detector.get_anomaly_summary(results)
    
    return results, summary

# Example usage
if __name__ == "__main__":
    # This would be used with actual data
    print("Sales Anomaly Detection Module")
    print("Use detect_sales_anomalies(df) to detect anomalies in your sales data")
