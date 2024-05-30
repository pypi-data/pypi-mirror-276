import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def handle_missing_values(df, strategy='mean'):
    """
    Handle missing values in the dataset using a specified strategy.
    """
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    if strategy == 'mean':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        for col in categorical_cols:
            mode_value = df[col].mode().values[0]
            df[col] = df[col].fillna(mode_value)
    elif strategy == 'median':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        for col in categorical_cols:
            mode_value = df[col].mode().values[0]
            df[col] = df[col].fillna(mode_value)
    elif strategy == 'mode':
        df = df.fillna(df.mode().iloc[0].to_numpy())
    elif strategy == 'drop':
        df = df.dropna()
    else:
        raise ValueError("Invalid strategy. Choose from 'mean', 'median', 'mode'")

    return df

def data_summary(df):
    """
    Print a summary of the dataset, including information about data types, missing values, and summary statistics.
    """
    print("Dataset Information:")
    print(df.info())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nSummary Statistics:")
    print(df.describe())


def plot_categorical_hist(df, col):
    """
    Plot a histogram for a categorical column.
    """
    value_counts = df[col].value_counts()
    categories = value_counts.index
    counts = value_counts.values
    plt.bar(categories, counts)
    plt.xticks(rotation=45)
    
def create_histograms(df):
    numerical_columns = df.select_dtypes(include=['int', 'float']).columns
    
    # Calculate number of rows and columns for subplots
    num_plots = len(numerical_columns)
    num_rows = (num_plots + 2) // 3  # Add 2 before dividing to ensure we have enough rows
    num_cols = 3  # Update number of columns for subplots
    
    # Create subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(18, 6 * num_rows))  # Adjust figsize for three plots per row
    axs = axs.flatten()  # Flatten the axs array to simplify indexing
    
    # Plot histograms
    for i, col in enumerate(numerical_columns):
        sns.histplot(data=df, x=col, bins=20, color='#c9e6f6', edgecolor='black', ax=axs[i])  # Changed color and edgecolor
        
        mean_value = df[col].mean()
        median_value = df[col].median()
        
        axs[i].axvline(mean_value, color='green', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')  # Changed color
        axs[i].axvline(median_value, color='purple', linestyle='dashed', linewidth=2, label=f'Median: {median_value:.2f}')  # Changed color
        
        axs[i].set_title(f"Distribution of {col} ", fontsize=16, fontweight='bold')  # Changed title font size and weight
        axs[i].set_xlabel(col, fontsize=12)  # Changed x-axis label font size
        axs[i].set_ylabel("Frequency", fontsize=12)  # Changed y-axis label
        
        axs[i].legend(fontsize=10)  # Changed legend font size
        
        axs[i].grid(axis='y', color='gray')  # Added grid lines for better readability
        
    # Hide empty subplots
    for j in range(num_plots, num_rows * num_cols):
        axs[j].axis('off')
        
    plt.tight_layout()  # Adjust layout for better spacing
    plt.show() 


def plot_correlation(df, figsize=(10, 8), missing_strategy='mean'):
     """
     Plot a correlation matrix heatmap for the dataset.
     """
     # Handle missing values
     data_filled = df.handle_missing_values(strategy=missing_strategy)
 
     # Create a DataFrame with only numeric columns
     numeric_cols = data_filled.select_dtypes(include=['float64', 'int64']).columns
     numeric_data = data_filled[numeric_cols]
 
     plt.figure(figsize=figsize)
     corr = numeric_data.corr()
     plt.imshow(corr, cmap='coolwarm')
     plt.colorbar()
     plt.xticks(range(len(corr)), corr.columns, rotation=90)
     plt.yticks(range(len(corr)), corr.columns)
     plt.title('Correlation Matrix')
     plt.show()
     
def categorical_analysis(df, col):
    """
    Analyze a categorical column by printing its value counts and plotting a bar chart.
    """
    print(f"Value Counts for {col}:")
    print(df[col].value_counts())
    plt.figure(figsize=(8, 6))
    df.plot_categorical_hist(col)
    plt.title(f"Distribution of {col}")
    plt.show()

def create_boxplots(df):
    numerical_columns = df.select_dtypes(include=['int', 'float']).columns
    
    # Calculate number of rows and columns for subplots
    num_plots = len(numerical_columns)
    num_rows = (num_plots + 2) // 3  # Add 2 before dividing to ensure we have enough rows
    num_cols = 3  # Update number of columns for subplots
    
    # Create subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(18, 6 * num_rows))  # Adjust figsize for three plots per row
    axs = axs.flatten()  # Flatten the axs array to simplify indexing
    
    # Plot box plots
    for i, col in enumerate(numerical_columns):
        sns.boxplot(data=df[col], ax=axs[i], color='#c9e6f6')  # Changed color
        
        mean_value = df[col].mean()
        median_value = df[col].median()
        
        axs[i].axhline(mean_value, color='green', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')  # Changed color
        axs[i].axhline(median_value, color='purple', linestyle='dashed', linewidth=2, label=f'Median: {median_value:.2f}')  # Changed color
        
        axs[i].set_title(f"Boxplot of {col} ", fontsize=16, fontweight='bold')  # Changed title font size and weight
        axs[i].set_xlabel(col, fontsize=12)  # Changed x-axis label font size
        axs[i].set_ylabel("Value", fontsize=12)  # Changed y-axis label
        
        axs[i].legend(fontsize=10)  # Changed legend font size
        
    # Hide empty subplots
    for j in range(num_plots, num_rows * num_cols):
        axs[j].axis('off')
        
    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()



