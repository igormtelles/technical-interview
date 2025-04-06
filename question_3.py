"""
Question 3: Sales Visualization

Using the cleaned dataset from Question 1 ('sales_data.csv'), create the following visualizations:

1. Create a line plot showing daily sales trends over time
   - Include a 7-day moving average line

2. Create a bar plot showing:
   - Total sales by category
   - Include error bars representing standard deviation

3. Create a scatter plot showing:
   - Relationship between quantity and price
   - Color points by category
   - Add a trend line

Requirements:
- Use appropriate labels and titles
- Include a legend where necessary
- Use a consistent color scheme
- Save all plots as PNG files
"""

# import of necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates           # customizar ticks com datas
from matplotlib.ticker import FuncFormatter # customizar ticks com datas
import seaborn as sns
import numpy as np

# Reading the sales dataset cleand in question 1
sales_df = pd.read_csv("../data/sales_data_cleaned.csv")
# Converting 'date_sale' to datetime type
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'], errors='coerce')


"""
1. Create a line plot showing daily sales trends over time
   - Include a 7-day moving average line

Here a line plot is created to visualize the daily sales trends over time.
Each data point represents the total sales value for a specific day.
To smooth out daily fluctuations and highlight
underlying trends, a 7-day moving average is applied. The plot includes:
- A line for raw daily sales
- A line for the 7-day moving average
- Custom ticks on the x-axis for years (major) and specific months (minor)
- A dark-themed, publication-ready style
Finally, the plot is saved as a high-resolution PNG file.
"""

# File name to save the figure
nome_png = 'daily_sales.png'

# Defining the moving average window size (in days)
window_size = 7

# Aggregating total sales per day based on quantity sold (not revenue)
# Each row is a transaction, and we're counting how many units were sold per day
daily_sales = sales_df.groupby('sale_date')['quantity'].sum()

# Separating X and Y for plotting
x = daily_sales.index
y = daily_sales.values

# Calculating the moving average over the defined window
y_average = daily_sales.rolling(window=window_size).mean()

# Seting plot style
plt.style.use('seaborn-v0_8')

# Creating figure and axis
fig, ax1 = plt.subplots(1, 1, figsize=(12, 6), sharex=True)

# Ploting raw daily sales (quantity sold)
ax1.plot(x, y, label='Time series data', alpha=0.5, color='plum')

# Ploting 7-day moving average
ax1.plot(x, y_average, label=f'{window_size}-day moving average', color='indigo')

# Adding title and axis labels
ax1.set_title(f'Daily sales with {window_size}-day moving average', loc='left', fontsize=18, pad=15)
ax1.set_xlabel('Date', fontsize=14, labelpad=12)
ax1.set_ylabel('Total Sales', fontsize=14, labelpad=12)

# Y-axis scale adjusted to show all values clearly
ax1.set_ylim(0, 11)
ax1.tick_params(axis='y', labelsize=10, length=5)

# Adding legend
ax1.legend(fontsize=12, loc='upper right')

# Adding gridlines
ax1.grid(True)

# Configuration of major x-axis ticks (years)
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Configuration of minor x-axis ticks (months: March, June, September, December)
ax1.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 6, 9, 12]))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax1.tick_params(axis='x', which='minor', length=5, color='gray', labelsize=8)

# Rotating x-axis tick labels for better readability
ax1.tick_params(axis='x', rotation=45)

# Saving the plot as PNG with high resolution
plt.savefig(nome_png, dpi=300)
print('------------ END OF ITEM 1------------\n')
print('\n')


"""
2. Create a bar plot showing:
   - Total sales by category
   - Include error bars representing standard deviation

Now, a bar plot that shows the total sales per product category is created.
In addition to the total amount, the standard deviation of sales
within each category and use it as error bars is calculate.

The plot includes:
- Bars representing total sales per category
- Error bars for the standard deviation
- Custom axis labels and styling
"""
# File name to save the figure
nome_png = 'bar_plot.png'

# Grouping data by category: calculate total quantity sold and standard deviation
category_stats = sales_df.groupby('category')['quantity'].agg(['sum', 'std']).sort_values(by='sum', ascending=False)

# Extracting metrics for plotting
categories = category_stats.index                 # Category names (x-axis)
totals = category_stats['sum']                    # Total quantity sold per category (bar height)
errors = category_stats['std']                    # Standard deviation per category (error bars)

# Creating figure and axis
fig, ax2 = plt.subplots(figsize=(10, 6))

# Ploting bar chart with error bars
ax2.bar(
    categories,
    totals,
    yerr=errors,              # Error bars using standard deviation
    capsize=18,               # Adds end caps to error bars
    ecolor='black',           # Error bar color
    color='darkorchid',       # Bar color
    alpha=0.8                 # Bar transparency
)

# Adding title and axis labels
ax2.set_title('Total Sales by Category with Standard Deviation', loc='left', fontsize=18, pad=12)
ax2.set_xlabel('Category', fontsize=14, labelpad=12)
ax2.set_ylabel('Total Sales', fontsize=14, labelpad=12)

# Rotating x-axis labels for readability
plt.xticks(rotation=45, ha='right')

# Adding horizontal grid lines for better readability
ax2.grid(axis='y', linestyle='--', alpha=0.5)

# Adjusting layout to avoid label clipping
plt.tight_layout()

# Saveing plot as PNG file with high resolution
plt.savefig(nome_png, dpi=300)
print('------------ END OF ITEM 2------------\n')
print('\n')


"""
3. Create a scatter plot showing:
   - Relationship between quantity and price
   - Color points by category
   - Add a trend line

A scatter plot is created to explore the relationship between the quantity of items sold and their unit price.
Each point in the plot represents a transaction, with different colors used to distinguish between product categories.
To help visualize general pricing trends across all categories, a global linear trend line is computed using least squares
regression and overlaid on the plot.
"""

# File name to save the figure
nome_png = 'scatter_plot.png'

# Creating figure and axis for the scatter plot
fig, ax3 = plt.subplots(figsize=(12, 6))

# Getting unique categories to assign distinct colors for each
categories = sales_df['category'].unique()
colors = plt.cm.tab10.colors  # Colormap for up to 10 distinct colors

# Plotting one scatter series per category with its assigned color
for i, cat in enumerate(categories):
    subset = sales_df[sales_df['category'] == cat]
    ax3.scatter(
        subset['quantity'],    # X-axis: quantity sold
        subset['price'],       # Y-axis: price per unit
        label=cat,             # Legend label
        color=colors[i % len(colors)],
        alpha=0.65,            # Transparency
        s=50                   # Point size
    )

# Computing linear regression (trend line) across all data points
x = sales_df['quantity']
y = sales_df['price']
slope, intercept = np.polyfit(x, y, 1)                      # Linear regression
x_vals = np.linspace(x.min(), x.max(), 100)                 # X-axis for trend line
y_vals = slope * x_vals + intercept                         # Corresponding Y values

# Plotting the global trend line
ax3.plot(x_vals, y_vals, color='black', linewidth=1.5, label='Trend Line')

# Customizing title and axis labels
ax3.set_title('Relationship between Quantity and Price by Category', fontsize=18, loc='left', pad=12)
ax3.set_xlabel('Quantity Sold', fontsize=14, labelpad=12)
ax3.set_ylabel('Price per Unit', fontsize=14, labelpad=12)

# Setting legend outside the plot to the right
ax3.legend(
    title='Category',
    bbox_to_anchor=(1.0, 0.7),
    loc='upper left',
    borderaxespad=0
)

# Adding grid lines for better readability
ax3.grid(True)

# Adjusting layout to prevent label clipping
plt.tight_layout()

# Saving the plot as a high-resolution PNG file
plt.savefig(nome_png, dpi=300)
print('------------ END OF ITEM 3------------\n')
print('\n')
print('Please, don’t forget to check the final comment at the end of the code')
print('Igor M. Telles :)')


"""
In the bar plot, the error bars are very small and barely visible.
Removing them might make the visualization cleaner and more visually appealing, in my opinion.
"""
