from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FATWA_CSV_PATH = BASE_DIR / "data" / "fatwas.csv"
QURAN_INDEX_PATH = BASE_DIR / "indexing" / "quran_index"
HADITH_INDEX_PATH = BASE_DIR / "indexing" / "hadith_index"
FATWAS_INDEX_PATH = BASE_DIR / "indexing" / "fatwas_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
