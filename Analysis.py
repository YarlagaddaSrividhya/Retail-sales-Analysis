import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# optional for nicer plots
import seaborn as sns
sns.set()   # uses default seaborn style

df = pd.read_csv('sales.csv')
df.head()
# shape & types
print(df.shape)
print(df.dtypes)

# nulls
print(df.isnull().sum())

# duplicates
print("duplicates:", df.duplicated().sum())
df = df.drop_duplicates()
df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')  # convert, bad parse -> NaT
df = df.dropna(subset=['OrderDate'])  # drop rows with invalid date if any

# create revenue
df['Revenue'] = df['Quantity'] * df['UnitPrice']
total_revenue = df['Revenue'].sum()
total_orders = df['OrderID'].nunique()
total_customers = df['CustomerID'].nunique()
avg_order_value = df.groupby('OrderID')['Revenue'].sum().mean()

print(f"Total revenue: {total_revenue:.2f}")
print(f"Orders: {total_orders}, Customers: {total_customers}")
print(f"Average order value: {avg_order_value:.2f}")
df['Month'] = df['OrderDate'].dt.to_period('M')  # e.g. 2024-03
monthly = df.groupby('Month')['Revenue'].sum().reset_index()
monthly['Month'] = monthly['Month'].dt.to_timestamp()  # for plotting

plt.figure(figsize=(10,4))
plt.plot(monthly['Month'], monthly['Revenue'], marker='o')
plt.title('Monthly Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
top_products = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(10)
print(top_products)

top_categories = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
print(top_categories)
top_products.plot(kind='bar', figsize=(8,4))
plt.title('Top 10 Products by Revenue')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()
top_customers = df.groupby('CustomerID')['Revenue'].sum().sort_values(ascending=False).head(10)
print(top_customers)
orders_per_customer = df.groupby('CustomerID')['OrderID'].nunique()
repeat_ratio = (orders_per_customer > 1).mean()  # fraction of customers with >1 order
print("Repeat customer ratio:", repeat_ratio)
# First purchase month per customer
first_order = df.groupby('CustomerID')['OrderDate'].min().dt.to_period('M').rename('first_month')
df = df.join(first_order, on='CustomerID')
cohort = df.groupby(['first_month', df['OrderDate'].dt.to_period('M')])['CustomerID'].nunique().unstack(fill_value=0)
cohort.head()
df.to_csv('sales_cleaned.csv', index=False)
monthly.to_csv('monthly_revenue.csv', index=False)
