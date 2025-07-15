from core.services import search_quran, search_hadith, search_fatwa
import json
from core.logger import logger


def quran_tool(query: str):
    logger.info(f"Query sent to Quran tool is:\n{query}\n")
    results = search_quran(query, k=3)
    logger.info(f"Result of quran tool is:\n{results}\n")
    return json.dumps(results, indent=2, ensure_ascii=False)

def hadith_tool(query: str):
    logger.info(f"Query sent to Hadith tool is:\n{query}\n")
    results = search_hadith(query, k=3)
    logger.info(f"Result of hadith tool is:\n{results}\n")
    return json.dumps(results, indent=2, ensure_ascii=False)

def fatwa_tool(query: str):
    logger.info(f"Query sent to Fatwa tool is:\n{query}\n")
    results = search_fatwa(query, k=3)
    logger.info(f"Result of fatwa tool is:\n{results}\n")
    return json.dumps(results, indent=2, ensure_ascii=False)
