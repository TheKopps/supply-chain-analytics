from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_POWERBI = PROJECT_ROOT / "data" / "powerbi"

SALES_ANALYTICS_PATH = DATA_PROCESSED / "sales_analytics.csv"
SALES_CLEAN_PATH = DATA_PROCESSED / "sales_clean.csv"
SALES_FEATURED_PATH = DATA_PROCESSED / "sales_featured.csv"

REPORTS_PATH = PROJECT_ROOT / "reports"
FIGURES_PATH = REPORTS_PATH / "figures"
INSIGHTS_PATH = REPORTS_PATH / "insights"
