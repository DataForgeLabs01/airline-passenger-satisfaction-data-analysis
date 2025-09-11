from pathlib import Path

RAW_PATH = Path(r"C:/Users/alikm/OneDrive/Masaüstü/projects/ortak/airline-passenger-satisfaction-data-analysis/data/raw/raw-data.csv")
PROCESSED_DIR = Path(r"C:/Users/alikm/OneDrive/Masaüstü/projects/ortak/airline-passenger-satisfaction-data-analysis/data/processed")
PROCESSED_PATH = PROCESSED_DIR / "processed.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# List of columns to drop
DROP_COLUMNS = ["Unnamed: 0", "id"]

# Column to impute missing values
IMPUTE_COLUMN = "Arrival Delay in Minutes"
