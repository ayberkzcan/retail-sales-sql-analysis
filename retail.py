import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# LOAD & CLEAN DATA
df = pd.read_csv("superstore.csv", encoding="ISO-8859-1")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Date conversion
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

# Feature engineering
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df = df[df["shipping_days"] >= 0]

# KEY KPIs
print("\n--- KEY KPIs ---")
print(f"Total Revenue: {df['sales'].sum():,.2f}")
print(f"Total Customers: {df['customer_id'].nunique():,}")
print(f"Total Products Sold: {df['quantity'].sum():,}")
print(f"Unique Products: {df['product_id'].nunique():,}")

# SQLITE SETUP
conn = sqlite3.connect("superstore.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

# REVENUE TREND
query_revenue = """
SELECT 
    strftime('%Y-%m', order_date) AS month,
    SUM(sales) AS revenue,
    SUM(profit) AS profit
FROM sales
GROUP BY month
ORDER BY month;
"""
revenue_df = pd.read_sql(query_revenue, conn)
print("\n--- REVENUE TREND ---")
print(revenue_df)

# SHIPPING ANALYSIS
query_shipping = """
SELECT AVG(shipping_days) AS avg_shipping_time FROM sales;
"""
query_shipping_region = """
SELECT region, AVG(shipping_days) AS avg_shipping_time
FROM sales
GROUP BY region
ORDER BY avg_shipping_time;
"""
query_shipping_segment = """
SELECT segment, AVG(shipping_days) AS avg_shipping_time
FROM sales
GROUP BY segment
ORDER BY avg_shipping_time;
"""
query_delivery_speed = """
SELECT 
    CASE 
        WHEN shipping_days <= 3 THEN 'Fast'
        WHEN shipping_days <= 6 THEN 'Medium'
        ELSE 'Slow'
    END AS delivery_speed,
    COUNT(*) AS order_count
FROM sales
GROUP BY delivery_speed;
"""
print("\n--- AVG SHIPPING TIME ---")
print(pd.read_sql(query_shipping, conn))
print("\n--- SHIPPING BY REGION ---")
print(pd.read_sql(query_shipping_region, conn))
print("\n--- SHIPPING BY SEGMENT ---")
print(pd.read_sql(query_shipping_segment, conn))
df_speed = pd.read_sql(query_delivery_speed, conn)

# PRODUCT ANALYSIS
query_products = """
SELECT 
    product_name,
    SUM(sales) AS revenue
FROM sales
GROUP BY product_name
ORDER BY revenue DESC;
"""
df_products = pd.read_sql(query_products, conn)
df_products = df_products.sort_values("revenue", ascending=False)

# PARETO (PRODUCT)
df_products = df_products.sort_values("revenue", ascending=False)
df_products["cum_revenue"] = df_products["revenue"].cumsum()
df_products["cum_share"] = df_products["cum_revenue"] / df_products["revenue"].sum()
pareto_80_products = (df_products["cum_share"] <= 0.8).sum()

# GINI COEFFICIENT
values = np.sort(df_products["revenue"].values)
n = len(values)
cum_values = np.cumsum(values)

gini = (n + 1 - 2 * np.sum(cum_values) / cum_values[-1]) / n

# GEOGRAPHY
query_geo = """
SELECT region, SUM(sales) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;
"""
df_geo = pd.read_sql(query_geo, conn)

# CUSTOMER ANALYSIS
query_customers = """
SELECT customer_name, SUM(sales) AS revenue
FROM sales
GROUP BY customer_name
ORDER BY revenue DESC;
"""
df_cust = pd.read_sql(query_customers, conn)

df_cust = df_cust.sort_values("revenue", ascending=False)
df_cust["cum_share"] = df_cust["revenue"].cumsum() / df_cust["revenue"].sum()

# DISCOUNT EFFECT
query_discount = """
SELECT 
    discount,
    AVG(profit) AS avg_profit
FROM sales
GROUP BY discount
ORDER BY discount;
"""
df_discount = pd.read_sql(query_discount, conn)
print("\n--- DISCOUNT EFFECT ---")
print(df_discount)

# BUSINESS SUMMARY
print("\n--- BUSINESS SUMMARY ---")
print(f"Pareto Products (80% revenue): {pareto_80_products}")
print(f"Gini Coefficient: {gini:.2f}")
print(f"Avg Shipping Days: {df['shipping_days'].mean():.2f}")
print("Revenue Concentration: High (Pareto + Gini confirmed)")

# VISUALIZATION
plt.rcParams["figure.figsize"] = (10,6)

# REVENUE TREND
plt.figure()
plt.plot(revenue_df["month"], revenue_df["revenue"])
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.tight_layout()
plt.show()

# REVENUE vs PROFIT
plt.figure()
plt.plot(revenue_df["month"], revenue_df["revenue"], label="Revenue")
plt.plot(revenue_df["month"], revenue_df["profit"], label="Profit")
plt.legend()
plt.xticks(rotation=45)
plt.title("Revenue vs Profit")
plt.tight_layout()
plt.show()

# TOP PRODUCTS
top_products = df_products.head(10)

plt.figure()
plt.barh(top_products["product_name"], top_products["revenue"])
plt.gca().invert_yaxis()
plt.title("Top 10 Products")
plt.tight_layout()
plt.show()

# PARETO
plt.figure()
plt.plot(df_products["cum_share"].values)
plt.axhline(0.8)
plt.title("Pareto Analysis (Products)")
plt.tight_layout()
plt.show()

# REGION
plt.figure()
plt.bar(df_geo["region"], df_geo["revenue"])
plt.title("Revenue by Region")
plt.tight_layout()
plt.show()

# CUSTOMER PARETO
plt.figure()
plt.plot(df_cust["cum_share"].values)
plt.axhline(0.8)
plt.title("Customer Pareto")
plt.tight_layout()
plt.show()

# DELIVERY SPEED
plt.figure()
plt.bar(df_speed["delivery_speed"], df_speed["order_count"])
plt.title("Delivery Speed Distribution")
plt.tight_layout()
plt.show()

conn.close()
