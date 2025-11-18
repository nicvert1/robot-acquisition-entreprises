import requests
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
from supabase import create_client, Client
from datetime import datetime, timezone
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SERP_API_KEY = os.getenv("SERPAPI_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_company(name, link):
    try:
        payload = {
            "nom_entreprise": name,
            "lien": link,
            "score_evaluation": 0,
            "date": datetime.now(timezone.utc).isoformat()
        }
        print("[SUPABASE] Payload:", payload)
        res = supabase.table("companies").insert(payload).execute()
        print("[SUPABASE] Saved:", link)
    except Exception as e:
        print("[SUPABASE ERROR]", e)

def scrape_companies(query):
    print("[SEARCH] Searching:", query)
    search = GoogleSearch({
        "q": query,
        "engine": "google",
        "api_key": SERP_API_KEY,
        "num": 10
    })
    results = search.get_dict()

    if "organic_results" not in results:
        print("[ERROR] No results")
        return

    for r in results["organic_results"]:
        title = r.get("title")
        link = r.get("link")
        if title and link:
            print("[FOUND]", title, "|", link)
            save_company(title, link)

def main():
    sectors = ["ébénisterie", "usinage", "fabrication métallique", "soudure"]
    city = "Blainville"

    for sector in sectors:
        query = f"{sector} entreprise {city}"
        scrape_companies(query)

if __name__ == "__main__":
    print("[ROBOT] Started")
    main()
    print("[ROBOT] Completed")
