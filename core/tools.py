from langchain_core.tools import tool
from core.services import search_quran, search_hadith, search_fatwa
import json
from core.logger import logger

@tool
def quran_tool(query: str) -> str:
    """
    Search the Quran for verses related to the user's query.
    Always use this tool when the user asks about Quranic rulings, verses, or Islamic principles found in the Quran.
    """
    logger.info(f"Query sent to Quran tool is:\n{query}\n")
    results = search_quran(query, k=3)
    logger.info(f"Result of quran tool is:\n{results}\n")
    return json.dumps(results, indent=2, ensure_ascii=False)

@tool
def hadith_tool(query: str) -> str:
    """
    Search the Hadith for sayings and actions of Prophet Muhammad (PBUH) related to the user's query.
    Always use this tool when the user asks about Hadiths, prophetic traditions, or Sunnah.
    """
    logger.info(f"Query sent to Hadith tool is:\n{query}\n")
    results = search_hadith(query, k=3)
    logger.info(f"Result of hadith tool is:\n{results}\n")
    return json.dumps(results, indent=2, ensure_ascii=False)

@tool
def fatwa_tool(query: str) -> str:
    """
    Search scholarly Islamic Fatwas (rulings) related to the user's query.
    Use this tool when the user asks for scholarly opinions, rulings on specific contemporary issues, or fatwas.
    """
    logger.info(f"Query sent to Fatwa tool is:\n{query}\n")
    results = search_fatwa(query, k=3)
    logger.info(f"Result of fatwa tool is:\n{results}\n")
    return json.dumps(results, indent=2, ensure_ascii=False)
