# src/analysis_b/distance_satisfaction.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from matplotlib.patches import Patch

def load_and_prepare(path: Path) -> pd.DataFrame:
    """Load dataset, select relevant columns, and prepare satisfaction labels"""
    df = pd.read_csv(path)
    
    # Keep only relevant columns
    sub = df[["Flight Distance", "satisfaction"]].copy()
    
    # Map to numeric 0/1
    mapping = {"neutral or dissatisfied": 0, "satisfied": 1}
    sub["satisfaction_num"] = sub["satisfaction"].str.lower().map(mapping)
    
    # Map to human-readable labels
    label_map = {0: "Neutral/Dissatisfied", 1: "Satisfied"}
    sub["satisfaction_label"] = sub["satisfaction_num"].map(label_map)
    
    # Categorical with fixed order
    order = ["Neutral/Dissatisfied", "Satisfied"]
    sub["satisfaction_label"] = pd.Categorical(
        sub["satisfaction_label"], categories=order, ordered=True
    )
    
    return sub

def compute_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute summary statistics (count, mean, median, std)"""
    stats = df.groupby("satisfaction_label", observed=False)["Flight Distance"].agg(
        ["count", "mean", "median", "std"]
    ).round(2)
    return stats

def plot_figures(df: pd.DataFrame, fig_path: Path):
    """Create scatter, boxplot, and histogram and save the figure"""
    order = ["Neutral/Dissatisfied", "Satisfied"]
    palette = {"Neutral/Dissatisfied": "red", "Satisfied": "green"}
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    
    # Scatter (sampled)
    sns.scatterplot(
        data=df.sample(3000, random_state=42),
        x="Flight Distance",
        y="satisfaction_label",
        hue="satisfaction_label",
        hue_order=order,
        palette=palette,
        alpha=0.3,
        s=15,
        ax=axes[0],
        legend=False
    )
    axes[0].set_title("Scatter (sampled & colored)")
    axes[0].set_ylabel("Satisfaction")
    
    # Boxplot
    sns.boxplot(
        data=df,
        x="satisfaction_label",
        y="Flight Distance",
        hue="satisfaction_label",
        hue_order=order,
        dodge=False,
        legend=False,
        palette=palette,
        ax=axes[1]
    )
    axes[1].set_title("Boxplot by Satisfaction")
    axes[1].set_xlabel("Satisfaction")
    
    # Histogram (draw groups separately to fix colors)
    bin_edges = np.histogram_bin_edges(df["Flight Distance"], bins=40)
    
    sns.histplot(
        data=df[df["satisfaction_label"] == "Neutral/Dissatisfied"],
        x="Flight Distance",
        bins=bin_edges,
        stat="density",
        element="step",
        alpha=0.4,
        color=palette["Neutral/Dissatisfied"],
        ax=axes[2]
    )
    sns.histplot(
        data=df[df["satisfaction_label"] == "Satisfied"],
        x="Flight Distance",
        bins=bin_edges,
        stat="density",
        element="step",
        alpha=0.4,
        color=palette["Satisfied"],
        ax=axes[2]
    )
    custom_legend = [
        Patch(facecolor=palette["Neutral/Dissatisfied"], alpha=0.4, label="Neutral/Dissatisfied"),
        Patch(facecolor=palette["Satisfied"], alpha=0.4, label="Satisfied")
    ]
    axes[2].legend(handles=custom_legend, title="Satisfaction")
    axes[2].set_title("Histogram of Flight Distance by Satisfaction")
    
    plt.suptitle("Flight Distance vs Satisfaction Analysis", fontsize=16, y=1.05)
    plt.tight_layout()
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, dpi=300)
    plt.close(fig)

def save_stats(stats: pd.DataFrame, tbl_path: Path):
    """Save summary stats to CSV"""
    tbl_path.parent.mkdir(parents=True, exist_ok=True)
    stats.to_csv(tbl_path)

def main():
    # Resolve repo root based on current file location
    repo_root = Path(__file__).resolve().parents[2]  # go 2 levels up from src/analysis_b
    
    input_path = repo_root / "data" / "processed" / "processed.csv"
    fig_path = repo_root / "reports" / "figures" / "flight_distance_satisfaction.png"
    tbl_path = repo_root / "reports" / "tables" / "flight_distance_satisfaction_stats.csv"
    
    df = load_and_prepare(input_path)
    stats = compute_stats(df)
    plot_figures(df, fig_path)
    save_stats(stats, tbl_path)
    
    print("Analysis completed.")
    print("Figure saved to:", fig_path)
    print("Table saved to:", tbl_path)

if __name__ == "__main__":
    main()
