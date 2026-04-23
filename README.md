# 📦 Superstore Retail Analysis (SQL + Python)

## 🧠 Overview
End-to-end retail analysis using SQL and Python to evaluate revenue drivers, profitability, and operational efficiency.

This project focuses on understanding how revenue, profit, and business concentration behave across products, customers, and time.

Key finding: Revenue grows steadily, but profitability is highly sensitive to discounts and business is strongly concentrated.

## 🛠️ Tools
- Python (Pandas, NumPy, Matplotlib)
- SQLite (SQL queries via Python)
- Data Analysis & Visualization

## 📊 Dataset
- ~10,000 transactions  
- 793 customers  
- 1,862 products  
- Multi-year retail data  

## 📈 Key KPIs
- Total Revenue: 2.29M  
- Total Customers: 793  
- Unique Products: 1,862  
- Units Sold: 37,873  
- Avg Shipping Time: ~3.96 days  

## 📊 Key Insights

### 📈 Revenue Trend
- Stable upward growth over time
- Strong seasonality (Q4 peaks every year)
👉 Revenue growth does not always lead to higher profit

### 💸 Profitability & Discounts
- 0–10% discount → positive profit
- 20–30% discount → reduced margins
- 30%+ discount → frequent losses
👉 Profitability is strongly dependent on discount strategy

### 🛒 Product Concentration (Pareto Analysis)
- ~419 products generate 80% of total revenue
👉 Revenue is driven by a small subset of products

### 📉 Revenue Concentration (Gini = 0.73)
👉 High inequality in revenue distribution across products

### 👥 Customer Concentration
- Small group of customers generates majority of revenue
👉 High dependency on top customers

### 📦 Operations (Shipping)
- Average shipping time: ~3.96 days
- Minor regional differences
- Overall stable logistics performance
👉 Logistics is not a major bottleneck

## 💡 Business Recommendations
- Reduce dependency on high discounts (>30%)
- Focus on top-performing products (Pareto group)
- Diversify customer base to reduce concentration risk
- Maintain current logistics efficiency

## 🧠 Final Conclusion
- Revenue is growing steadily 📈  
- Profitability is inconsistent 💸  
- Business is highly concentrated ⚠️  
- Operations are stable 📦  
👉 Core issue: imbalance between growth and profitability structure

## 🚀 Impact
- SQL + Python integrated analysis  
- Business insight generation  
- Advanced metrics (Pareto, Gini)  
- End-to-end analytical thinking beyond reporting  
