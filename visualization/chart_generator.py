import os
import matplotlib.pyplot as plt
import pandas as pd

def create_bar_chart(df: pd.DataFrame, cat_col: str, num_col: str, output_path: str) -> str:
    """
    Generates a static bar chart showing total sum of a numeric column grouped by a categorical column.
    Saves the output as a PNG file.
    """
    # 1. Aggregate the raw data using Pandas grouping
    grouped_data = df.groupby(cat_col)[num_col].sum()
    categories = grouped_data.index.tolist()
    values = grouped_data.values.tolist()
    
    # 2. Set up the Matplotlib canvas drawing arena
    # figsize=(8, 5) creates a landscape image 8 inches wide by 5 inches tall
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 3. Draw the bars onto the grid axes
    ax.bar(categories, values, color='teal', edgecolor='black', width=0.6)
    
    # 4. Apply clean titles and label layouts
    ax.set_title(f"Total {num_col.replace('_', ' ')} by {cat_col.replace('_', ' ')}", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(cat_col.replace('_', ' '), fontsize=11, labelpad=10)
    ax.set_ylabel(f"Sum of {num_col.replace('_', ' ')}", fontsize=11, labelpad=10)
    
    # Enable faint horizontal grid lines behind the bars to help readability
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True) 
    
    # 5. Automatically adjust spacing so text margins don't get cut off
    plt.tight_layout()
    
    # Ensure destination directories exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 6. Save out to a static PNG image and close the canvas to save RAM
    plt.savefig(output_path, dpi=150)
    plt.close(fig)
    
    return output_path


def create_pie_chart(df: pd.DataFrame, cat_col: str, output_path: str) -> str:
    """
    Generates a static pie chart representing percentage allocations of items inside a category.
    Saves the output as a PNG file.
    """
    # 1. Use value_counts() to measure frequency of groups
    counts = df[cat_col].value_counts()
    labels = counts.index.tolist()
    sizes = counts.values.tolist()
    
    # 2. Build canvas easel setup (uniform dimensions work best for circular charts)
    fig, ax = plt.subplots(figsize=(6, 6)) 
    
    # 3. Draw out slices
    # autopct='%1.1f%%' calculates percentages automatically and shows them inside slices
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, 
           colors=['#4f81bd', '#c0504d', '#9bbb59'], 
           wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True})
    
    # 4. Apply title
    ax.set_title(f"Distribution of {cat_col.replace('_', ' ')} Records", fontsize=14, fontweight='bold', pad=15)
    
    # Adjust alignment
    plt.tight_layout()
    
    # Ensure destination directories exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 5. Export and clear figure instance
    plt.savefig(output_path, dpi=150)
    plt.close(fig)
    
    return output_path