from pathlib import Path

# === BASE DIR ===
BASE_DIR = Path(__file__).resolve().parent.parent  # src/ -> project root

# === PATHS ===
RAW_PATH = BASE_DIR / "data" / "raw" / "raw-data.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_PATH = PROCESSED_DIR / "processed.csv"

# === Ensure Output Dir Exists ===
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# === Cleaning Settings ===
DROP_COLUMNS = ["Unnamed: 0", "id"]
IMPUTE_COLUMN = "Arrival Delay in Minutes"
