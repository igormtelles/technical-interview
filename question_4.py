"""
Question 4: Statistical Analysis and Error Handling

Using scipy and the cleaned dataset from Question 1, perform the following tasks:

1. Implement error handling for the following analyses:
   - Perform a one-way ANOVA test to compare prices across different categories
   - Calculate and plot the confidence intervals for mean prices in each category
   - Identify potential outliers using z-scores

2. Debug and fix the following code snippet that attempts to perform a chi-square test:
   ```python
   def perform_chi_square(data):
       observed = data.groupby(['category', 'status']).size()
       chi2, p_value = stats.chi2_contingency(observed)
       return chi2, p_value
   ```

3. Implement proper logging to track:
   - Any statistical assumptions violations
   - Data type mismatches
   - Invalid calculations

Your solution should be robust against various edge cases and include appropriate error messages.
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import logging


nome_png = 'confidence_interval.png'


# ------------------------------------------------------------------------------
# Setting up logging to capture info, warnings, and errors
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Loading the cleaned dataset (adjust the file path if needed)
sales_df = pd.read_csv("../data/sales_data_cleaned.csv")

# Ensuring that the 'sale_date' is parsed as datetime and 'category' is a string
sales_df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
sales_df['category'] = sales_df['category'].astype(str)

"""
1. Implement error handling for the following analyses:
   - Perform a one-way ANOVA test to compare prices across different categories
   - Calculate and plot the confidence intervals for mean prices in each category
   - Identify potential outliers using z-scores
"""

# 1. One-way ANOVA test to compare prices across different categories

def perform_anova(data, value_col='price', group_col='category'):

    """
    Performs a one-way ANOVA test to compare the mean prices across different categories.

    The function does the following:
      - Drops rows with missing values in the specified columns.
      - Checks that there are at least two distinct groups to compare.
      - Groups the data by the specified group column (category) and extracts the values
        from the value column ('price') for each group.
      - Applies the one-way ANOVA test (using scipy.stats.f_oneway) to the grouped data.
      - Logs information, warnings, or errors throughout the process.

    Parameters:
      data (DataFrame): The input DataFrame containing the data.
      value_col (str): The name of the column containing the values to compare (default 'price').
      group_col (str): The name of the column to group by (default 'category').

    Returns:
      tuple: A tuple containing the F-statistic and p-value, or None if an error occurs.
    """
    try:
        # Checking and droping rows with missing values in the key columns
        if data[value_col].isnull().any() or data[group_col].isnull().any():
            logging.warning("Missing values detected in ANOVA inputs; dropping affected rows.")
            data = data.dropna(subset=[value_col, group_col])

        # Ensurinf there are at least two distinct groups for the ANOVA test
        if data[group_col].nunique() < 2:
            logging.error("ANOVA requires at least two groups. Not enough groups found.")
            return None

        # Grouping data by the group column and collect the value column as arrays
        groups = [group[value_col].values for name, group in data.groupby(group_col)]

        # Performign one-way ANOVA test
        f_stat, p_value = stats.f_oneway(*groups)

        # Logging success and return the test results
        logging.info(f"ANOVA completed successfully. F-statistic = {f_stat:.4f}, p-value = {p_value:.4f}")
        return f_stat, p_value
    except Exception as e:
        # Logginng any errors that occur during the computation
        logging.error(f"Error during ANOVA: {e}")
        return None

# Running the ANOVA test on the 'price' column grouped by 'category'
anova_result = perform_anova(sales_df, value_col='price', group_col='category')
if anova_result is not None:
    f_stat, p_val = anova_result
    # Converting NumPy float values to standard Python floats for cleaner printing
    print("ANOVA Results: F-statistic = {:.4f}, p-value = {:.4f}".format(float(f_stat), float(p_val)))
else:
    print("ANOVA test failed.")

# Calculating and plotting the confidence intervals for mean prices in each category
def compute_confidence_intervals(data, value_col='price', group_col='category', confidence=0.95):

    """
    Computes the confidence intervals for the mean price in each category.
    Returns a DataFrame with columns: category, mean, lower CI, and upper CI.
    """
    ci_list = []
    try:
        for cat, group in data.groupby(group_col):
            values = group[value_col].dropna()
            n = len(values)
            if n < 2:
                logging.warning(f"Not enough data for category '{cat}' to compute a confidence interval.")
                continue
            mean_val = np.mean(values)
            sem_val = stats.sem(values)
            margin = sem_val * stats.t.ppf((1 + confidence) / 2., n - 1)
            ci_list.append((cat, mean_val, mean_val - margin, mean_val + margin))
        ci_df = pd.DataFrame(ci_list, columns=[group_col, 'mean', 'ci_lower', 'ci_upper'])
        return ci_df
    except Exception as e:
        logging.error(f"Error computing confidence intervals: {e}")
        return None

ci_df = compute_confidence_intervals(sales_df, value_col='price', group_col='category', confidence=0.95)
if ci_df is not None:
    print("\nConfidence Intervals for Mean Prices by Category:")
    print(ci_df)

    """
    # Plotting the confidence intervals
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.errorbar(ci_df['category'], ci_df['mean'], yerr=[ci_df['mean'] - ci_df['ci_lower'], ci_df['ci_upper'] - ci_df['mean']],
                fmt='o', capsize=5, color='darkorchid')
    ax.set_title('95% Confidence Intervals for Mean Prices by Category', fontsize=18, loc='left', pad=15)
    ax.set_xlabel('Category', fontsize=14)
    ax.set_ylabel('Mean Price', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(nome_png, dpi=300)
    """

else:
    print("Confidence interval calculation failed.")


# Identifing potential outliers using z-scores in the 'price' column
def detect_outliers_zscore(data, value_col='price', threshold=3.0):

    """
    Identifies potential outliers in the specified column using z-scores.
    Returns a DataFrame of rows where the absolute z-score exceeds the threshold.
    """
    try:
        values = data[value_col].dropna()
        z_scores = stats.zscore(values)
        outlier_indices = values.index[np.abs(z_scores) > threshold]
        outliers = data.loc[outlier_indices]
        return outliers
    except Exception as e:
        logging.error(f"Error during outlier detection: {e}")
        return None

outliers_df = detect_outliers_zscore(sales_df, value_col='price', threshold=3.0)
if outliers_df is not None and not outliers_df.empty:
    print("\nPotential Outliers (using z-scores on 'price'):")
    print(outliers_df[['sale_id', 'category', 'price']])
else:
    print("No significant outliers detected or outlier detection failed.")
print('------------ END OF ITEM 1------------\n')
print('\n')

"""
2. Debug and fix the following code snippet that attempts to perform a chi-square test:
   ```python
   def perform_chi_square(data):
       observed = data.groupby(['category', 'status']).size()
       chi2, p_value = stats.chi2_contingency(observed)
       return chi2, p_value
   ```
"""
def perform_chi_square(data):

    """
    Performs a chi-square test for independence between 'category' and 'status'.

    The function does the following:
      - Checks if the required columns ('category' and 'status') are present. If not, it logs an error.
      - Drops rows with missing values in these required columns.
      - Creates a contingency table by grouping the data by 'category' and 'status',
        using unstack(fill_value=0) to fill missing groups with zero.
      - Checks that the contingency table has at least two rows and two columns.
      - Performs the chi-square test using scipy.stats.chi2_contingency.

    Returns:
      A tuple (chi2, p_value) if the test is successful, or None if an error occurs.
    """
    try:
        # Define the required columns for the test
        required_cols = ['category', 'status']
        # Check if any required column is missing; if so, log an error and return None
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            logging.error(f"Missing required column(s): {', '.join(missing_cols)}")
            return None

        # Drop any rows with missing values in the required columns
        data_clean = data.dropna(subset=required_cols)
        if data_clean.empty:
            logging.error("Data is empty after dropping missing values in required columns.")
            return None

        # Create a contingency table by grouping the data by 'category' and 'status'
        # Unstack the grouped data to convert it into a 2D table, filling missing values with 0
        observed = data_clean.groupby(['category', 'status']).size().unstack(fill_value=0)
        # Check that the table has at least two groups (rows and columns) for a valid chi-square test
        if observed.empty or observed.shape[0] < 2 or observed.shape[1] < 2:
            logging.error("Contingency table is not suitable for a chi-square test (not enough groups).")
            return None

        # Perform the chi-square test on the contingency table
        chi2, p_value, dof, expected = stats.chi2_contingency(observed)
        logging.info(f"Chi-square test completed successfully. Chi2 = {chi2:.4f}, p-value = {p_value:.4f}")
        return chi2, p_value

    except Exception as e:
        # Log any unexpected error during the computation
        logging.error(f"An error occurred during the chi-square test: {e}")
        return None

# For the chi-square test, ensure a 'status' column is available.
# Here, we create a dummy 'status' column based on the 'quantity' column:
# If the quantity is greater than 5, label as 'High'; otherwise, label as 'Low'
sales_df['status'] = np.where(sales_df['quantity'] > 5, 'High', 'Low')

# Run the chi-square test function on the sales data
chi2_results = perform_chi_square(sales_df)
if chi2_results is not None:
    chi2_val, chi2_p = chi2_results
    # Convert NumPy float values to Python floats for a cleaner print output
    print("Chi-square Test Results: Chi2 = {:.4f}, p-value = {:.4f}".format(float(chi2_val), float(chi2_p)))
else:
    print("Chi-square test failed.")

print('------------ END OF ITEM 2------------\n')
print('Please, don’t forget to check the final comments at the end of the code')
print('Igor M. Telles :)')



"""
Here are some thougts about the results:

ANOVA Results:
The one-way ANOVA test produced a high p-value (for example, around 0.81), which indicates that
there is no statistically significant difference in the mean prices across the different product categories.
In other words, the variation in prices between categories is similar to the variation within each category.

Confidence Intervals:
The computed 95% confidence intervals for the mean prices of each category largely overlap.
This further supports the ANOVA result, suggesting that any differences in average price are not statistically meaningful.
The overlapping intervals imply that the true mean prices for these categories might be quite similar.

Potential Outliers:
Outlier detection using z-scores identified a few transactions with unusually low or high prices.
While these outliers do not alter the overall finding from the ANOVA (since they represent only a small fraction of the data),
they might warrant further investigation. For example, an extremely low or high price might be due to data entry errors, special promotions,
or unique product features that are not representative of the typical category pricing.
"""
