import cloudscraper
import json
import streamlit as st

def fetch_search_results(query, key):
    scraper = cloudscraper.create_scraper()
    url = "https://aappapi.investing.com/search_by_type.php"
    params = {
        "section": "quotes",
        "string": query,
        "lang_ID": 1,
    }
    headers = {"x-meta-ver": "14"}

    response = scraper.get(url, params=params, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            suggestions = {
                f"{item['search_main_longtext']} {item['search_main_subtext']}": {
                    "pair_ID": item['pair_ID'],
                    "search_main_longtext": item['search_main_longtext']
                }
                for item in data['data']['quotes']
            }
            st.session_state[f"suggestions_{key}"] = suggestions
            return list(suggestions.keys())
        except json.JSONDecodeError:
            return ["Failed to decode JSON"]
    else:
        return [f"Request failed with status code {response.status_code}"]