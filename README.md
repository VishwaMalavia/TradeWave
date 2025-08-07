📈 TradeWave – Stock Market Analysis & Admin Dashboard

TradeWave is a Python-based CLI (Command-Line Interface) application designed for administrative management and analytical visualization of stock market data. It uses MySQL as the backend database and Matplotlib for graphical stock trend analysis.

🚀 Features
✅ Admin Panel
Secure Login (with username and password)
Manage Stock Data
Add New Stock Entry
Update Stock Details
Delete Stock Entry
View All Stocks

📊 Stock Analysis Tools
Line Chart: View price trends with dynamic green/red plotting
Bar Chart: Compare open vs. close prices with colored bars
Candlestick Chart: Financial-style visualization of stock movement
Revenue Growth Analysis: Monthly aggregation with chart selection (Line/Bar/Pie)
Depth Level Analysis: Price volatility chart (High - Low)

🛠️ Setup Instructions
1. 🔧 Prerequisites
    Python 3.x
    MySQL via XAMPP 
    Required Python packages:  pip install mysql-connector-python matplotlib numpy

2. 🗄️ Import Database
  1.Open phpMyAdmin or MySQL CLI.
  2.Create the database:
      CREATE DATABASE stockmarketdb;
  3.Import stockmarketdb.sql to populate admin and stocklist tables.

3. 🧪 Run the Application
    python TradeWave.py

🔐 Admin Login
Username: admin
Password: password123

💡 Sample Use Case Flow
1. Start the App
2. Choose: Admin Login or Analyze Stock Trends
3. If Admin:Add, Update, or Delete stocks
4. If Analyst:
   Select from 5 different chart types
   Input stock symbol (e.g., AAPL, MSFT, GOOG)
   Visualize insights
