"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

Bonus: Identify any customers who haven't made a purchase in the last 3 months
"""

# import of necessary libraries
import pandas as pd

"""
Before addressing the specific tasks, we'll first explore the dataset using a 
similar approach to the one implemented in question_1.py.
"""

# reading the data set
purchase_df = pd.read_csv("../data/customer_purchases.csv")

# checking the first lines
print('First lines of the data set:')
print(purchase_df.head())
print('\n')

# checking properties of the data set
print('Number of lines and columns:', purchase_df.shape)           
print('Amount of missing values:', purchase_df.isna().sum().sum()) 
print('Variable types:')
print(purchase_df.dtypes)
print('\n')

"""
While there are no missing values, we need to convert the purchase_date column to datetime format for proper analysis.
"""

# Converting 'purchase_sale' to datetime type
purchase_df['purchase_date'] = pd.to_datetime(purchase_df['purchase_date'], errors='coerce')


"""
1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

In order to compute the metrics above, the dataset is grouped by 'customer_id' and then the metrics are computed.
"""

# Grouping the dataset by 'customer_id' and sum the 'amount' column,
grouped = purchase_df.groupby('customer_id').agg(
    total_spent=('amount', 'sum'),
    average_purchase=('amount', 'mean'),
    num_purchases=('amount', 'count'),
    most_frequent_category=('category', lambda x: x.mode().iloc[0] if not x.mode().empty else None)
).reset_index()


print("The following metrics are per customer (for the first 3 customers)\n")
print('\nTotal amount spent:\n', total_spent.head(3))
print('\nAverage purchase value:\n', average_purchase.head(3))
print('\nNumber of purchases:\n', num_purchase.head(3))
print('\nMost frequently bought category:\n', most_frequent_category.head(3))
print('------------ END OF ITEM 1------------\n')


"""
2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

To identify the top and bottom spenders among all customers, the following steps are performed:
 - Sort the customer-level metrics by total amount spent
 - Select the top 5 and bottom 5 customers based on spending
 - Combine both groups into a single summary DataFrame
"""

# Sorting the grouped item by 'total_spent' in descending order
# to find the top spenders
sorted_customers = grouped.sort_values(by='total_spent', ascending=False)

# Geting Top and Bottom 5 customers
top_5 = sorted_customers.head(5).copy()
top_5['position'] = 'Top 5'

bottom_5 = sorted_customers.tail(5).copy()
bottom_5['position'] = 'Bottom 5'

# Combining and reorder columns
summary_df = pd.concat([top_5, bottom_5], ignore_index=True)
summary_df = summary_df[['position', 'customer_id', 'total_spent', 'average_purchase', 'num_purchases', 'most_frequent_category']]

# Results!
print("Summary of Top 5 and Bottom 5 Customers by Total Spending:")
print(summary_df[['position', 'customer_id', 'total_spent']])
print('------------ END OF ITEM 2------------\n')

"""
3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

To analyze monthly trends in customer purchases, a new column is created to represent each transaction's year 
and month and then calculate:
 - The total amount spent per month
 - The average value of individual purchases per month  
"""

# Creating a new column with just the year and month 
purchase_df['month'] = purchase_df['purchase_date'].dt.to_period('M')

# Total amount spent per month
total_sales_month = purchase_df.groupby('month')['amount'].sum()

# Average purchase value per month
average_purchase_month = purchase_df.groupby('month')['amount'].mean()

print("Total sales per month:")
print(total_sales_month.head())

print("\nAverage purchase value per month:")
print(average_purchase_month.head())
print('------------ END OF ITEM 3------------\n')

"""
Bonus: Identify any customers who haven't made a purchase in the last 3 months

To identify customers who haven't made any purchases in the last 3 months, the performed steps are
 - Determine the date of the most recent purchase in the dataset
 - Calculate the cutoff date (3 months before the latest purchase)
 - Find customers whose most recent purchase is earlier than the cutoff
"""

# Latest purchase date in the dataset
latest_date = purchase_df['purchase_date'].max()

# Defining the cutoff date (3 months before the latest purchase)
cutoff_date = latest_date - pd.DateOffset(months=3)

# Finding the last purchase date for each customer
last_purchase_dates = purchase_df.groupby('customer_id')['purchase_date'].max().reset_index()

# Identifing customers whose last purchase was before the cutoff
inactive_customers = last_purchase_dates[last_purchase_dates['purchase_date'] < cutoff_date]

# Results!
print(f"Customers inactive since before {cutoff_date.date()}:\n")
print(inactive_customers)
print('------------ END OF BONUS ITEM------------\n')
print('\n')
print('Igor M. Telles :)')
