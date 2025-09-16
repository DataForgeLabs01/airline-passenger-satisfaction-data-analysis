import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------
# Load Data
# ----------------------
def load_data(file_path):
    """Load the processed airline satisfaction dataset."""
    df = pd.read_csv(file_path)
    return df

# ----------------------
# Preprocessing
# ----------------------
def add_satisfaction_column(df):
    """Add binary satisfaction column (1 = satisfied, 0 = not satisfied)."""
    df['satisfied'] = np.where(df['satisfaction'] == 'satisfied', 1, 0)
    return df

# ----------------------
# Correlation with satisfaction
# ----------------------
def calculate_correlation(df, service_cols):
    """Calculate correlation of services with satisfaction (in %)."""
    corr = df[service_cols + ['satisfied']].corr()
    corr_percent = corr['satisfied'][service_cols] * 100
    return corr_percent.sort_values(ascending=False)

# ----------------------
# Vertical Bar Chart
# ----------------------
def plot_correlation_bar(corr_percent):
    """Plot vertical bar chart of service correlations with satisfaction."""
    labels = corr_percent.index
    x = np.arange(len(labels))
    width = 0.5

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, corr_percent.values, width, label='Correlation with Satisfaction')

    ax.set_ylabel('Correlation (%)')
    ax.set_title('Service Factors Correlated with Satisfaction')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)  # labels horizontal
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Annotate values
    for i, v in enumerate(corr_percent.values):
        ax.text(x[i], v + 0.5, f"{v:.1f}%", ha='center', va='bottom', fontsize=9)

    # Most/least correlated text
    most_corr = corr_percent.idxmax()
    least_corr = corr_percent.idxmin()
    plt.subplots_adjust(bottom=0.2)
    fig.text(
        0.5, 0.05,
        f"Most correlated: {most_corr} | Least correlated: {least_corr}",
        ha='center', va='center',
        fontsize=11, fontweight='bold'
    )

    plt.show()

# ----------------------
# Pie Chart
# ----------------------
def plot_correlation_pie(corr_percent):
    """Pie chart of service correlations with satisfaction."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        corr_percent.values, 
        labels=corr_percent.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=plt.cm.Paired.colors
    )
    ax.set_title("Service Correlation with Satisfaction (Pie Chart)")
    plt.show()

# ----------------------
# Horizontal Bar Chart
# ----------------------
def plot_correlation_hbar(corr_percent):
    """Horizontal bar chart of service correlations with satisfaction."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(corr_percent.index, corr_percent.values, color='skyblue')
    ax.set_xlabel("Correlation (%)")
    ax.set_title("Service Factors Correlated with Satisfaction")
    for i, v in enumerate(corr_percent.values):
        ax.text(v + 0.5, i, f"{v:.1f}%", va='center', fontsize=9)
    plt.show()

# ----------------------
# Main Workflow
# ----------------------
def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "processed" / "processed.csv"
    service_cols = ['Ease of Online booking','Seat comfort','Baggage handling','Cleanliness','Inflight service']

    # Load and prepare data
    df = load_data(file_path)
    df = add_satisfaction_column(df)

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df[service_cols + ['satisfaction', 'satisfied']].head())

    # Correlation calculation
    corr_percent = calculate_correlation(df, service_cols)
    print("Service correlation with satisfaction:\n", corr_percent)

    # Plot vertical bar chart
    plot_correlation_bar(corr_percent)

    # Plot pie chart
    plot_correlation_pie(corr_percent)

    # Plot horizontal bar chart
    plot_correlation_hbar(corr_percent)

if __name__ == "__main__":
    main()
