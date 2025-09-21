"""
AI-Powered Sales Insights Generator
Generates intelligent insights and recommendations from sales data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SalesInsightsGenerator:
    def __init__(self):
        """Initialize the insights generator"""
        self.insights = []
        
    def generate_trend_insights(self, df):
        """Generate insights about sales trends"""
        insights = []
        
        # Monthly trend analysis
        monthly_sales = df.groupby(['YEAR', 'MONTH'])['SALES'].sum().reset_index()
        monthly_sales['date'] = pd.to_datetime(monthly_sales[['YEAR', 'MONTH']].assign(DAY=1))
        
        # Calculate month-over-month growth
        monthly_sales['mom_growth'] = monthly_sales['SALES'].pct_change() * 100
        
        # Find best and worst months
        best_month = monthly_sales.loc[monthly_sales['SALES'].idxmax()]
        worst_month = monthly_sales.loc[monthly_sales['SALES'].idxmin()]
        
        insights.append({
            'type': 'trend',
            'title': 'Monthly Performance',
            'insight': f"Best performing month: {best_month['MONTH']:02d}/{best_month['YEAR']} with ${best_month['SALES']:,.2f} in sales",
            'recommendation': 'Analyze what made this month successful and replicate strategies',
            'impact': 'high'
        })
        
        insights.append({
            'type': 'trend',
            'title': 'Monthly Performance',
            'insight': f"Lowest performing month: {worst_month['MONTH']:02d}/{worst_month['YEAR']} with ${worst_month['SALES']:,.2f} in sales",
            'recommendation': 'Investigate factors that led to poor performance and develop recovery strategies',
            'impact': 'medium'
        })
        
        # Year-over-year analysis
        yearly_sales = df.groupby('YEAR')['SALES'].sum()
        if len(yearly_sales) > 1:
            yoy_growth = ((yearly_sales.iloc[-1] - yearly_sales.iloc[-2]) / yearly_sales.iloc[-2]) * 100
            
            if yoy_growth > 0:
                insights.append({
                    'type': 'trend',
                    'title': 'Year-over-Year Growth',
                    'insight': f"Sales grew by {yoy_growth:.1f}% compared to previous year",
                    'recommendation': 'Maintain current strategies and consider scaling successful initiatives',
                    'impact': 'high'
                })
            else:
                insights.append({
                    'type': 'trend',
                    'title': 'Year-over-Year Decline',
                    'insight': f"Sales declined by {abs(yoy_growth):.1f}% compared to previous year",
                    'recommendation': 'Urgent action needed to reverse declining trend',
                    'impact': 'critical'
                })
        
        return insights
    
    def generate_product_insights(self, df):
        """Generate insights about product performance"""
        insights = []
        
        product_sales = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False)
        total_sales = product_sales.sum()
        
        # Top performer
        top_product = product_sales.index[0]
        top_product_share = (product_sales.iloc[0] / total_sales) * 100
        
        insights.append({
            'type': 'product',
            'title': 'Product Performance',
            'insight': f"'{top_product}' is the top performer with {top_product_share:.1f}% of total sales (${product_sales.iloc[0]:,.2f})",
            'recommendation': 'Increase marketing and inventory for this product line',
            'impact': 'high'
        })
        
        # Underperformer
        bottom_product = product_sales.index[-1]
        bottom_product_share = (product_sales.iloc[-1] / total_sales) * 100
        
        if bottom_product_share < 5:  # Less than 5% market share
            insights.append({
                'type': 'product',
                'title': 'Product Performance',
                'insight': f"'{bottom_product}' is underperforming with only {bottom_product_share:.1f}% of total sales",
                'recommendation': 'Consider discontinuing or rebranding this product line',
                'impact': 'medium'
            })
        
        return insights
    
    def generate_customer_insights(self, df):
        """Generate insights about customer behavior"""
        insights = []
        
        customer_analysis = df.groupby('CUSTOMERNAME').agg({
            'SALES': 'sum',
            'ORDERNUMBER': 'count',
            'QUANTITYORDERED': 'sum'
        }).reset_index()
        
        customer_analysis.columns = ['customer', 'total_sales', 'order_count', 'total_quantity']
        customer_analysis['avg_order_value'] = customer_analysis['total_sales'] / customer_analysis['order_count']
        
        # Top customer
        top_customer = customer_analysis.loc[customer_analysis['total_sales'].idxmax()]
        
        insights.append({
            'type': 'customer',
            'title': 'Customer Value',
            'insight': f"'{top_customer['customer']}' is the highest value customer with ${top_customer['total_sales']:,.2f} in total sales",
            'recommendation': 'Implement VIP program and personalized service for high-value customers',
            'impact': 'high'
        })
        
        # Customer loyalty analysis
        repeat_customers = customer_analysis[customer_analysis['order_count'] > 1]
        loyalty_rate = (len(repeat_customers) / len(customer_analysis)) * 100
        
        if loyalty_rate < 30:
            insights.append({
                'type': 'customer',
                'title': 'Customer Loyalty',
                'insight': f"Only {loyalty_rate:.1f}% of customers make repeat purchases",
                'recommight': 'Implement customer retention programs and loyalty incentives',
                'impact': 'high'
            })
        
        return insights
    
    def generate_all_insights(self, df):
        """Generate comprehensive insights from sales data"""
        all_insights = []
        
        # Generate insights from different perspectives
        all_insights.extend(self.generate_trend_insights(df))
        all_insights.extend(self.generate_product_insights(df))
        all_insights.extend(self.generate_customer_insights(df))
        
        # Sort by impact level
        impact_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        all_insights.sort(key=lambda x: impact_order.get(x['impact'], 4))
        
        return all_insights
    
    def format_insights_report(self, insights):
        """Format insights into a readable report"""
        if not insights:
            return "No insights generated."
        
        report = "# Sales Data Insights Report\n\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Group insights by type
        insight_types = {}
        for insight in insights:
            insight_type = insight['type']
            if insight_type not in insight_types:
                insight_types[insight_type] = []
            insight_types[insight_type].append(insight)
        
        # Generate report sections
        for insight_type, type_insights in insight_types.items():
            report += f"## {insight_type.title()} Insights\n\n"
            
            for i, insight in enumerate(type_insights, 1):
                impact_emoji = {
                    'critical': '🚨',
                    'high': '⚠️',
                    'medium': '📊',
                    'low': 'ℹ️'
                }.get(insight['impact'], '📋')
                
                report += f"### {impact_emoji} {insight['title']}\n"
                report += f"**Insight:** {insight['insight']}\n\n"
                report += f"**Recommendation:** {insight['recommendation']}\n\n"
                report += f"**Impact Level:** {insight['impact'].title()}\n\n"
                report += "---\n\n"
        
        return report

def generate_sales_insights(df):
    """
    Convenience function to generate comprehensive sales insights
    
    Args:
        df (pd.DataFrame): Sales data
        
    Returns:
        tuple: (insights_list, formatted_report)
    """
    generator = SalesInsightsGenerator()
    insights = generator.generate_all_insights(df)
    report = generator.format_insights_report(insights)
    
    return insights, report

# Example usage
if __name__ == "__main__":
    print("Sales Insights Generator Module")
    print("Use generate_sales_insights(df) to generate insights from your sales data")