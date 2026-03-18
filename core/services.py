from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import pandas as pd
from core.config import *
from core.logger import logger

# Load embedder once
embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Load Fatwa database once
logger.info("Loading Fatwa CSV...")
fatwa_df = pd.read_csv(FATWA_CSV_PATH)

# Load FAISS indices once
logger.info("Loading FAISS indices...")
quran_store = FAISS.load_local(QURAN_INDEX_PATH, embedder, allow_dangerous_deserialization=True)
hadith_store = FAISS.load_local(HADITH_INDEX_PATH, embedder, allow_dangerous_deserialization=True)
fatwa_store = FAISS.load_local(FATWAS_INDEX_PATH, embedder, allow_dangerous_deserialization=True)

def get_fatwa_answer_by_id(fatwa_id):
    row = fatwa_df[fatwa_df['id'] == int(fatwa_id)]
    return row.iloc[0]['answer'] if not row.empty else "Answer not found."

def search_quran(query, k=2):
    results = quran_store.similarity_search(query, k=k)
    return [
        {
            "surah_no": doc.metadata['surah_no'],
            "surah_name": doc.metadata['surah_name'],
            "ayah_no": doc.metadata['ayah_no'],
            "text": doc.page_content
        }
        for doc in results
    ]

def search_hadith(query, k=2):
    results = hadith_store.similarity_search(query, k=k)
    return [
        {
            "book": doc.metadata['book'],
            "chapter": doc.metadata['chapter'],
            "hadith_number": doc.metadata['hadith_number'],
            "text": doc.page_content
        }
        for doc in results
    ]

def search_fatwa(query, k=2):
    results = fatwa_store.similarity_search(query, k=k)
    return [
        {
            "fatwa_id": doc.metadata['id'],
            "question": doc.page_content,
            "answer": get_fatwa_answer_by_id(doc.metadata['id'])
        }
        for doc in results
    ]
