# 📊 Sales Data Dashboard - Assignment 3

A comprehensive sales analytics platform built with modern technologies for real-time data visualization and business intelligence.

## 🚀 Features

- **📈 Interactive Dashboard**: Real-time sales analytics with beautiful visualizations
- **🔧 Data Preprocessing**: Automated data cleaning and feature engineering
- **🌐 RESTful API**: Fast and scalable backend with multiple endpoints
- **🤖 AI-Powered Insights**: Anomaly detection and intelligent recommendations
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

```
arys-assignment3-saloni/
├── 📁 data/
│   ├── raw/               # Raw sales CSV data
│   └── processed/         # Cleaned and processed data
├── 📁 notebooks/
│   └── 01_preprocessing.ipynb   # Data preprocessing pipeline
├── 📁 backend/
│   ├── app.py             # FastAPI backend server
│   └── requirements.txt   # Python dependencies
├── 📁 frontend/
│   └── app.py             # Streamlit dashboard
├── 📁 ai/
│   ├── anomaly.py         # Anomaly detection module
│   └── insights.py        # AI insights generator
├── 📁 report/
│   └── final_report.md    # Project documentation
├── 📁 demo_video/
│   └── demo_script.md     # Demo video script
└── README.md              # This file
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit, Plotly
- **Data Processing**: Pandas, NumPy, Jupyter
- **AI/ML**: Scikit-learn, Isolation Forest
- **Visualization**: Plotly, Matplotlib, Seaborn

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd arys-assignment3-saloni
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd ../frontend
   pip install streamlit plotly requests
   ```

### Running the Application

1. **Start the Backend API**
   ```bash
   cd backend
   python app.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Frontend Dashboard**
   ```bash
   cd frontend
   streamlit run app.py
   ```
   The dashboard will be available at `http://localhost:8501`

3. **Run Data Preprocessing**
   ```bash
   jupyter notebook notebooks/01_preprocessing.ipynb
   ```

## 📊 API Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `/` | API status and available endpoints | - |
| `/kpis` | Key performance indicators | - |
| `/sales_over_time` | Time-series sales data | `period`, `year` |
| `/sales_by_category` | Product line performance | - |
| `/sales_by_country` | Geographic analysis | `limit` |
| `/top_customers` | Customer rankings | `limit` |
| `/order_status` | Order status distribution | - |
| `/data_summary` | Overall data summary | - |

## 🎯 Key Features

### Data Preprocessing
- ✅ Missing value handling
- ✅ Duplicate removal
- ✅ Date feature extraction
- ✅ Categorical normalization
- ✅ Data validation

### Backend API
- ✅ RESTful endpoints
- ✅ CORS enabled
- ✅ Error handling
- ✅ Data validation
- ✅ Sample data generation

### Frontend Dashboard
- ✅ Interactive charts
- ✅ Real-time filtering
- ✅ Responsive design
- ✅ Multi-tab interface
- ✅ Auto-refresh capability

### AI Components
- ✅ Anomaly detection
- ✅ Business insights
- ✅ Actionable recommendations
- ✅ Performance metrics

## 📈 Dashboard Tabs

1. **📈 Overview**: KPIs, sales trends, order status
2. **🏷️ Products**: Product line performance analysis
3. **🌍 Geography**: Country-wise sales distribution
4. **👥 Customers**: Top customer rankings and analysis
5. **📊 Analytics**: Advanced metrics and insights

## 🤖 AI Features

### Anomaly Detection
- Identifies unusual patterns in sales data
- Uses Isolation Forest algorithm
- Provides anomaly scores and severity levels
- Generates detailed anomaly reports

### Insights Generation
- Automated business insights
- Trend analysis and recommendations
- Customer behavior analysis
- Operational efficiency metrics

## 📋 Sample Data

The system includes sample data generation for testing purposes. The backend automatically creates realistic sales data if no CSV file is found.

## 🔧 Configuration

### Backend Configuration
- API runs on port 8000 by default
- CORS enabled for all origins
- Automatic sample data generation

### Frontend Configuration
- Dashboard runs on port 8501 by default
- Connects to backend at localhost:8000
- Auto-refresh every 30 seconds (optional)

## 📚 Documentation

- **Final Report**: `report/final_report.md`
- **Demo Script**: `demo_video/demo_script.md`
- **API Documentation**: Available at `http://localhost:8000/docs`

## 🚀 Deployment

### Local Development
1. Follow the Quick Start guide above
2. Ensure all dependencies are installed
3. Start backend and frontend services

### Production Deployment
- Use a production WSGI server (e.g., Gunicorn)
- Configure environment variables
- Set up proper database connections
- Implement authentication and authorization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of Assignment 3 for the ARYS course.

## 👨‍💻 Author

**Saloni Gupta**  
Assignment 3 - Sales Data Dashboard

## 🎯 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Email alerts for anomalies
- [ ] Export functionality (PDF, Excel)
- [ ] Machine learning predictions
- [ ] Mobile app development
- [ ] Cloud deployment (AWS/Azure)

---

**Status**: ✅ Production Ready  
**Last Updated**: December 2024