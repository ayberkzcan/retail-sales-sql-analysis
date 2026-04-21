import pandas as pd
import sqlite3

df = pd.read_csv("superstore.csv", encoding="ISO-8859-1")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print(df.head())
print("Shape: ",df.shape)
print(df.columns)
print(df.info())

df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df = df[df["shipping_days"] >= 0]

conn = sqlite3.connect("superstore.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
print(pd.read_sql("SELECT * FROM sales LIMIT 5", conn))

query = """
SELECT 
    strftime('%Y-%m', order_date) as month,
    SUM(sales) as revenue,
    SUM(profit) as profit
FROM sales
GROUP BY month
ORDER BY month;
"""

print(pd.read_sql(query, conn))

query = """
SELECT 
    AVG(shipping_days) as avg_shipping_time
FROM sales;
"""

print(pd.read_sql(query, conn))

query = """
SELECT 
    segment,
    AVG(shipping_days) as avg_shipping_time
FROM sales
GROUP BY segment
ORDER BY avg_shipping_time;
"""

print(pd.read_sql(query, conn))

query = """
SELECT 
    region,
    AVG(shipping_days) as avg_shipping_time
FROM sales
GROUP BY region
ORDER BY avg_shipping_time;
"""

print(pd.read_sql(query, conn))

query = """
SELECT 
    CASE 
        WHEN shipping_days <= 3 THEN 'Fast'
        WHEN shipping_days <= 6 THEN 'Medium'
        ELSE 'Slow'
    END as delivery_speed,
    COUNT(*) as order_count
FROM sales
GROUP BY delivery_speed;
"""

print(pd.read_sql(query, conn))
