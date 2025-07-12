from core.services import search_quran, search_hadith, search_fatwa
import json

def quran_tool(query: str):
    results = search_quran(query, k=3)
    return json.dumps(results, indent=2, ensure_ascii=False)

def hadith_tool(query: str):
    results = search_hadith(query, k=3)
    return json.dumps(results, indent=2, ensure_ascii=False)

def fatwa_tool(query: str):
    results = search_fatwa(query, k=3)
    return json.dumps(results, indent=2, ensure_ascii=False)
