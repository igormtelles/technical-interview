"""
Question 1: Data Cleaning and Basic Analysis

Using the provided dataset 'sales_data.csv', perform the following tasks:

1. Load and examine the dataset
2. Clean the data:
   - Handle missing values in the 'price' column (replace with mean)
   - Handle missing values in the 'category' column (replace with mode)
   - Convert 'sale_date' to datetime
3. Create a summary of:
   - Total number of sales per category
   - Average price per category
   - Number of missing values handled

The cleaned dataset should be ready for further analysis.
"""

# import of necessary libraries
import pandas as pd

"""
1. Load and examine the dataset

The dataset is loaded and analyzed using Python's pandas library (pd). The following checks are performed:
 - Dataset shape (rows × columns) -> (1000, 5)
 - Presence of missing values across columns -> (79)
 - Column data types -> (int64, object, object, float64, int64) respectively
 - Specific validation:
   - Confirm missing values are limited to the price and category columns -> (limited in price e category indeed)
   - Quantify the exact number of missing entries in each affected column -> (category: 30 and price: 49)
"""

# reading the data set
sales_df = pd.read_csv("../data/sales_data.csv")

# checking the first lines
print('First lines of the data set:')
print(sales_df.head())
print('\n')

# checking properties of the data set
print('Number of lines and columns:', sales_df.shape)           
print('Amount of missing values:', sales_df.isna().sum().sum()) 
print('Variable types:')
print(sales_df.dtypes)
print('\n')

# Let's check what are the columns with missing values and how many are missing in each column

## count missing values per column
missing_data = sales_df.isna().sum()
## keep only columns with missing values
missing_data = missing_data[missing_data > 0]

print("Columns with missing data: ")
print(missing_data)
print('------------ END OF ITEM 1------------\n')
"""
2. Clean the data:

First, we address the missing values in the category column. The missing values are going to be 
replaced by the mode of the column — the most frequent category. To ensure the imputation was done correctly, 
the following steps are done: 
1. Before filling, identify the row that contained a missing value in the 'category' column.
2. Save the index of that row for reference.
3. After filling, check the same row again to see if its value was replaced with the mode.
4. If the filled value equals the mode, the imputation is confirmed to be correct.


The mode of the category column is 'Electronics', this is going to fill the missing values in this column.
"""

# Step 1: Select a row where 'category' is missing (NaN)
# This helps us verify if the missing value is properly filled later
cat_before = sales_df[sales_df['category'].isna()].iloc[0]

# Step 2: Calculate the mode (most frequent value) of the 'category' column
# This value will be used to fill in the missing entries
mode_category = sales_df['category'].mode()[0]

# Step 3: Fill missing values in 'category' with the mode
sales_df['category'] = sales_df['category'].fillna(mode_category)

# Step 4: Access the same row after the replacement using its index
# We use the row's index from before to compare the value after filling
index = cat_before.name  # Get the original row index
cat_after = sales_df.loc[index, 'category']

# Step 5: Print results to validate the replacement
#print(f"Category BEFORE replacing: {cat_before['category']}")
#print(f"Category AFTER replacing: {cat_after}")
#print(f"Column mode: {mode_category}")
#print('\n')


"""
Once the missing values in category is solved, we can:
 - Compute the mean price for each category.
 - Use these means to fill in the missing values in the price column.

Instead of filling all missing prices with the overall mean, I chose to apply the following approach:
  - Fill each missing value using the mean **specific to its category**.

 Why use the mean per category?
  - Different product categories tend to have different price ranges.
  - Using the category-specific mean maintains internal consistency and avoids introducing distortions.
The validation strategy is similiar that the one done for the category column:
1. Before filling, a row where the 'price' was missing is selected.
2. Saved the index and the corresponding category of that row.
3. After the imputation, check the new value at the same index.
4. Compare it to the mean price of that row's category.
5. If the values match, the imputation was successful.

Category         mean price
Books            101.690430
Clothing         103.822460
Electronics      100.468345
Home & Garden    102.661415
Sports           101.188330

"""

# Step 1: Select a row with a missing price
price_before = sales_df[sales_df['price'].isna()].iloc[0]
index = price_before.name  # Save the index to access the same row later
category = price_before['category']  # Save the corresponding category

# Step 2: Calculate the mean price per category and apply it to missing values
sales_df['price'] = sales_df.groupby('category')['price'].transform(lambda x: x.fillna(x.mean()))
mean_price_by_category = sales_df.groupby('category')['price'].mean()
#print('Mean price by category:')
#print(mean_price_by_category)

# Step 3: Access the same row (by index) after filling
price_after = sales_df.loc[index, 'price']

# Step 4: Calculate the expected mean of the category (for comparison)
expected_mean = sales_df[sales_df['category'] == category]['price'].mean()

# Step 5: Print results to validate the imputation
#print(f"Price BEFORE replacing: {price_before['price']}")
#print(f"Price AFTER replacing: {price_after}")
#print(f"Expected mean (category '{category}'): {expected_mean:.2f}")

# Converting 'date_sale' to datetime type
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'], errors='coerce')
#print(sales_df.dtypes)
print('To view the information described in the comments, please enable the print statements\n')
print('------------ END OF ITEM 2------------\n')


"""
3. Create a summary of:
   - Total number of sales per category
   - Average price per category
   - Number of missing values handled
   
Now the final task is handle the itens above. 
Then, save a new dataset file 'sales_data_cleaned.csv' for next questions.

"""

# Count total number of sales per category
# Assumes each row represents a single sale
total_number_per_category = sales_df.groupby('category')['quantity'].sum()
print("Total number of sales per category:")
print(total_number_per_category)
print('\n')

# Recalculate the average price per category (as previously done in step 2)
# This is repeated here for summary and reporting purposes
mean_price_per_category = sales_df.groupby('category')['price'].mean()
print("Mean price per category:")
print(mean_price_per_category)
print('\n')

# Calculate how many missing values were handled
# Earlier (in step 1), it was identified 79 missing values in total across 'price' and 'category'
# Now we compare cleaned dataset to determine how many values are missing
print('Amount of missing values:', sales_df.isna().sum().sum()) 
print('\n')

# Saving the cleaned dataset to a new CSV file
sales_df.to_csv('../data/sales_data_cleaned.csv', index=False)
print("Cleaned data saved to 'sales_data_cleaned.csv' in ../data/")
print('------------ END OF ITEM 3------------\n')
print('\n')
print('Please, don’t forget to check the final comment at the end of the code')
print('Igor M. Telles :)')


"""
I followed the instruction to fill missing category values with the mode, but I’d be cautious with that in a real-world scenario 
— especially when price is also missing. It might introduce bias and distort category-based price summaries.
I’d suggest either flagging those rows as 'unknown' or, where possible, inferring category from price or other 
features. That could preserve more of the data’s integrity for further analysis.
"""
