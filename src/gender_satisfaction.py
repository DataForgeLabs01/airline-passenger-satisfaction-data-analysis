"""
Reproducible script: compute Gender × Satisfaction distribution
and export both a stacked bar chart and per-gender pie charts (+ CSV).

Usage (from repo root):
  - Module (recommended):  python -m src.analysis_b.gender_satisfaction
  - Direct file:           python src/analysis_b/gender_satisfaction.py
  - Options:
      --show        show plots on screen
      --no-save     do not write any files
      --suffix X    append suffix to filenames (e.g., v1)
      --timestamp   append datetime suffix (e.g., 20250101-153000)
      --open        open saved files with OS default apps
"""

# ---- TOP: dual-run import shim + fix CWD to repo root ----
import sys, os, math
from pathlib import Path

# ensure working directory is the repo root so relative output paths are stable
REPO_ROOT = Path(__file__).resolve().parent.parent  # .../repo
os.chdir(REPO_ROOT)

try:
    # Case 1: run as module → python -m src.analysis_b.gender_satisfaction
    from src.config import PROCESSED_PATH
except ModuleNotFoundError:
    # Case 2: run as script → python src/analysis_b/gender_satisfaction.py
    SRC_DIR = Path(__file__).resolve().parents[1]  # .../repo/src
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    from config import PROCESSED_PATH
# ---- end shim ----

import argparse
from datetime import datetime
import subprocess

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter
from matplotlib.patches import Patch

# ---------------------------------------------------------------------
# Configuration (colors, output paths)
# ---------------------------------------------------------------------

COLORS = {
    "Satisfied":   "#1B641F",  # dark green
    "Unsatisfied": "#751717",  # dark red
}

OUT_DIR_FIG = Path("reports/figures")
OUT_DIR_TAB = Path("reports/tables")
OUT_STACKED  = OUT_DIR_FIG / "gender_satisfaction_stacked_pandas_clean.png"
OUT_PIES     = OUT_DIR_FIG / "gender_satisfaction_pies_clean.png"
OUT_TABLE    = OUT_DIR_TAB / "gender_satisfaction_percent.csv"


# ---------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    """Load the processed CSV defined in config."""
    # Read the processed CSV file into a DataFrame
    df = pd.read_csv(PROCESSED_PATH)
    return df


def map_satisfaction(df: pd.DataFrame) -> pd.DataFrame:
    """Map raw satisfaction values into two clean categories."""
    # Define a mapping dictionary for satisfaction categories
    mapper = {"satisfied": "Satisfied", "neutral or dissatisfied": "Unsatisfied"}
    # Create a new column 'SatisfactionBinary' with mapped values
    df["SatisfactionBinary"] = df["satisfaction"].map(mapper)
    return df


def get_gender_labels(df: pd.DataFrame) -> list[str]:
    """Choose an ordered list of gender categories present in data."""
    # Get unique gender values from the DataFrame
    present = df["Gender"].unique().tolist() 
    # Prioritize "Female" and "Male" categories if present
    base = [g for g in ["Female", "Male"] if g in present]
    # Include other gender categories in sorted order
    others = [g for g in sorted(present) if g not in {"Female", "Male"}]
    # Combine prioritized and other categories
    labels = base + others
    return labels


def compute_percent_table(df: pd.DataFrame, labels: list[str]) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """
    Compute counts and percentages by Gender × SatisfactionBinary.
    Returns (counts, pct, n_per_group).
    """
    # Create a contingency table for Gender and SatisfactionBinary
    counts = pd.crosstab(df["Gender"], df["SatisfactionBinary"]).reindex(labels)
    # Ensure both 'Satisfied' and 'Unsatisfied' columns exist
    for col in ["Satisfied", "Unsatisfied"]:
        if col not in counts.columns:
            counts[col] = 0
    # Reorder columns to maintain consistency
    counts = counts[["Satisfied", "Unsatisfied"]]
    # Calculate percentages for each gender
    pct = counts.div(counts.sum(axis=1), axis=0) * 100
    # Calculate total counts per gender
    n_per_group = counts.sum(axis=1)
    return counts, pct, n_per_group


# ---------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------

def plot_stacked_percent(
    pct: pd.DataFrame, save_path: Path, show: bool = False, save: bool = True
) -> "plt.Figure":
    """Draw polished stacked bar chart with in-bar % labels and (optionally) save/show."""
    # Set the plotting style
    plt.style.use("seaborn-v0_8-whitegrid")
    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

    # Plot the stacked bar chart with specified colors and formatting
    pct[["Satisfied", "Unsatisfied"]].plot(
        kind="bar", stacked=True, ax=ax,
        color=[COLORS["Satisfied"], COLORS["Unsatisfied"]],
        edgecolor="white", linewidth=0.6
    )

    # Set axis limits and labels
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))
    ax.set_ylabel("Percentage of passengers")
    ax.set_xlabel("Gender")
    ax.set_title("Satisfaction by Gender (Stacked, % Labels)", pad=12)
    ax.tick_params(axis="x", rotation=0)
    ax.set_axisbelow(True)

    # Add a legend outside the plot
    ax.legend(
        title="Satisfaction",
        bbox_to_anchor=(1.02, 1), loc="upper left",
        borderaxespad=0.0, frameon=False
    )

    # Add percentage labels inside the bars
    for i, g in enumerate(pct.index):
        s = float(pct.loc[g, "Satisfied"]); u = float(pct.loc[g, "Unsatisfied"])
        if s > 0:
            ax.text(i, s/2, f"{s:.1f}%", ha="center", va="center",
                    color="white", fontsize=9, fontweight="bold")
        if u > 0:
            ax.text(i, s + u/2, f"{u:.1f}%", ha="center", va="center",
                    color="white", fontsize=9, fontweight="bold")

    # Save the figure if required
    if save:
        OUT_DIR_FIG.mkdir(parents=True, exist_ok=True)
        fig.tight_layout(rect=[0, 0, 0.88, 1])
        fig.savefig(save_path, dpi=200, bbox_inches="tight")
    # Show the figure if required
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


def _grid_for_k(k: int) -> tuple[int, int]:
    """Choose a nice (rows, cols) grid for k pies."""
    # Determine grid layout based on the number of pies
    if k <= 3:
        return 1, k
    if k <= 6:
        return 2, 3
    cols = 3
    rows = math.ceil(k / cols)
    return rows, cols


def plot_pies(
    pct: pd.DataFrame, n_per_group: pd.Series, save_path: Path, show: bool = False, save: bool = True
) -> "plt.Figure":
    """Draw a grid of pies (one per gender) and (optionally) save/show."""
    # Determine the grid layout for the pies
    k = len(pct.index)
    rows, cols = _grid_for_k(k)

    # Set the plotting style
    plt.style.use("seaborn-v0_8-white")
    # Create a figure and axes for the pie charts
    fig, axes = plt.subplots(rows, cols, figsize=(5.5*cols, 4.2*rows), dpi=120)
    if isinstance(axes, np.ndarray):
        axes = axes.flatten()
    else:
        axes = np.array([axes])  # single axis case

    # Plot each pie chart
    for i, g in enumerate(pct.index):
        ax = axes[i]
        # Extract values for the pie chart
        values = pct.loc[g, ["Satisfied", "Unsatisfied"]].to_numpy()
        explode = (0.04, 0.04)  # slight 3D-like pop

        # Create the pie chart
        wedges, texts, autotexts = ax.pie(
            values, labels=None, autopct="%.1f%%", pctdistance=0.7,
            startangle=90, colors=[COLORS["Satisfied"], COLORS["Unsatisfied"]],
            explode=explode, shadow=True,
            wedgeprops={"linewidth": 1, "edgecolor": "white"}
        )

        # Customize the text inside the pie chart
        for t in autotexts:
            t.set_color("white"); t.set_fontweight("bold"); t.set_fontsize(9)

        # Set axis properties and title
        ax.axis("equal"); ax.grid(False)
        ax.set_title(f"{g} (n={int(n_per_group.loc[g])})", fontsize=11, pad=10)

    # Turn off unused axes if the grid is larger than the number of pies
    for j in range(i+1, rows*cols):
        axes[j].axis("off")

    # Add a shared legend outside the plot
    handles = [Patch(color=COLORS["Satisfied"], label="Satisfied"),
               Patch(color=COLORS["Unsatisfied"], label="Unsatisfied")]
    fig.legend(handles=handles, title="Satisfaction",
               loc="center right", bbox_to_anchor=(1.02, 0.5), frameon=False)

    # Save the figure if required
    if save:
        OUT_DIR_FIG.mkdir(parents=True, exist_ok=True)
        fig.suptitle("Satisfaction Distribution - Pie Charts by Gender",
                     fontsize=14, y=0.98)
        fig.tight_layout(rect=[0, 0, 0.88, 0.96])
        fig.savefig(save_path, dpi=200, bbox_inches="tight")
    # Show the figure if required
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


# ---------------------------------------------------------------------
# CLI / Orchestration
# ---------------------------------------------------------------------

def _open_file(path: Path) -> None:
    """Open a file with the OS default app (Windows/Mac/Linux)."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception:
        pass  # do not crash if open fails


def main() -> None:
    # ---- CLI args ----
    parser = argparse.ArgumentParser(description="Gender × Satisfaction charts exporter")
    parser.add_argument("--show", action="store_true", help="Display plots in windows")
    parser.add_argument("--no-save", action="store_true", help="Do not save any files")
    parser.add_argument("--suffix", type=str, default="", help="Append a suffix to filenames (e.g., v1)")
    parser.add_argument("--timestamp", action="store_true", help="Append a datetime suffix to filenames")
    parser.add_argument("--open", dest="open_files", action="store_true", help="Open saved files after writing")
    args = parser.parse_args()

    save_outputs = not args.no_save
    show_plots = args.show

    # Build filename suffix logic
    suffix_parts = []
    if args.suffix.strip():
        suffix_parts.append(args.suffix.strip())
    if args.timestamp:
        suffix_parts.append(datetime.now().strftime("%Y%m%d-%H%M%S"))
    suffix = "_".join(suffix_parts)

    def with_suffix(p: Path) -> Path:
        return p if not suffix else p.with_name(f"{p.stem}_{suffix}{p.suffix}")

    stacked_path = with_suffix(OUT_STACKED)
    pies_path    = with_suffix(OUT_PIES)
    table_path   = with_suffix(OUT_TABLE)

    # ---- pipeline ----
    df = load_data()
    df = map_satisfaction(df)
    labels = get_gender_labels(df)
    counts, pct, n_per_group = compute_percent_table(df, labels)

    # Save table
    if save_outputs:
        OUT_DIR_TAB.mkdir(parents=True, exist_ok=True)
        pct.to_csv(table_path)

    # Charts
    plot_stacked_percent(pct, stacked_path, show=show_plots, save=save_outputs)
    plot_pies(pct, n_per_group, pies_path, show=show_plots, save=save_outputs)

    if save_outputs:
        print(f"[OK] Saved table → {table_path}")
        print(f"[OK] Saved stacked chart → {stacked_path}")
        print(f"[OK] Saved pie charts → {pies_path}")

    if save_outputs and args.open_files:
        _open_file(stacked_path); _open_file(pies_path); _open_file(table_path)


if __name__ == "__main__":
    main()
