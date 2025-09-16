import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================
# Data Loading
# ==========================
def load_data(filepath):
    """Load CSV file into a pandas DataFrame"""
    df = pd.read_csv(filepath)
    return df

# ==========================
# Age Grouping
# ==========================
def age_to_group(age):
    """Convert numeric age to age group string"""
    if age <= 17:
        return '0-17'
    elif age <= 24:
        return '18-24'
    elif age <= 34:
        return '25-34'
    elif age <= 44:
        return '35-44'
    elif age <= 54:
        return '45-54'
    elif age <= 64:
        return '55-64'
    else:
        return '65+'

def add_age_group(df):
    """Add 'age_group' column to DataFrame"""
    df['age_group'] = df['Age'].apply(age_to_group)
    return df

# ==========================
# Satisfaction Categorization
# ==========================
def categorize_satisfaction(df):
    """Satisfaction values to simplified categories"""
    df['satisfaction_cat'] = np.where(df['satisfaction'] == 'satisfied', 'Satisfied', 'Unsatisfied')
    return df

# ==========================
# Percentage Calculation
# ==========================
def calculate_satisfaction_pct(df):
    """Calculate satisfaction percentages for each age group"""
    # Create a cross-tabulation table (like a pivot) between age_group (rows) and satisfaction_cat (columns)
    # → Shows how many people fall into each combination of age group and satisfaction category
    # normalize='index' → Instead of raw counts, convert each row into proportions (row sum = 1.0)
    # Multiplying by 100 → Turns proportions into percentages (% per age group)
    pct = pd.crosstab(df['age_group'], df['satisfaction_cat'], normalize='index') * 100
    pct = pct.round(1)
    return pct


# ==========================
# Plotting
# ==========================
def plot_satisfaction(pct):
    """Plot satisfaction percentages per age group"""
    age_groups = pct.index.tolist()
    categories = pct.columns.tolist()
    values = pct.values
    n_groups = len(age_groups)
    n_categories = len(categories)

    bar_width = 0.35
    x = np.arange(n_groups)

    fig, ax = plt.subplots(figsize=(12,6))
    colors = ['#1f77b4', '#ff7f0e']  # Satisfied: blue, Unsatisfied: orange

    # Draw bars for each category
    for i, cat in enumerate(categories):
        ax.bar(x + i*bar_width, values[:, i], width=bar_width, label=cat, color=colors[i])

    # Set X axis
    ax.set_xticks(x + bar_width/2)
    ax.set_xticklabels(age_groups, rotation=45, ha='right')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Age Group Satisfaction Analysis')
    ax.set_ylim(0, 100)
    ax.legend(title='Satisfaction')

    # Add percentage labels above bars
    for i in range(n_groups):
        for j in range(n_categories):
            val = values[i, j]
            ax.text(x[i] + j*bar_width, val + 1, f'{val:.1f}%', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()


# ==========================
# Main Execution
# ==========================
if __name__ == "__main__":
    filepath = "/Users/ahmethakan/Desktop/Mac/Yazılım/data analiz ortak/airline-passenger-satisfaction-data-analysis/data/processed/processed.csv"
    
    df = load_data(filepath)
    df = add_age_group(df)
    df = categorize_satisfaction(df)
    pct = calculate_satisfaction_pct(df)
    
    plot_satisfaction(pct)

