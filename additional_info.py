import cloudscraper
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import investgo as go

def get_infos(id):
    scraper = cloudscraper.create_scraper()
    url = "https://aappapi.investing.com/get_screen.php"
    params = {
        "screen_ID": 22,
        "pair_ID": id,
        "lang_ID": "1",
        "include_pair_attr": "true",
    }
    headers = {"x-meta-ver": "14"}

    response = scraper.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def extract_yield(eq_dividend_yield):
    if eq_dividend_yield:
        match = re.search(r'\(([\d\.]+)%\)', eq_dividend_yield)
        if match:
            return f"{match.group(1)}%"
    return '-'

def extract_data(json_data_list):
    df_list = []
    for json_data in json_data_list:
        if json_data and "data" in json_data:
            data = json_data["data"]
            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    screen_data = item.get('screen_data', {})
                    pairs_attr = screen_data.get('pairs_attr', [])
                    for attr in pairs_attr:
                        pair_name = attr.get("search_main_longtext")
                        pair_id = attr.get("pair_ID")
                        pair_symbol = attr.get("pair_symbol")
                        pairs_data = screen_data.get('pairs_data', [])
                        for pair in pairs_data:
                            # Fetch holdings data and check if it returns a valid list
                            try:   
                                holdings = go.get_holdings(pair_id)
                                df_sectors = holdings[2]
                                dominant_sector = df_sectors.loc[df_sectors['val'] > 40, 'fieldname']
                                category = dominant_sector.iloc[0] if not dominant_sector.empty else "Global Equity"
                            except Exception as e:
                                category = "Global Equity"
                            if pair.get("pair_ID") == pair_id:
                                pair_type = {"fund": "Fund", "etf": "ETF"}.get(pair.get("pair_type_section"), pair.get("pair_type_section"))
                                pair_info = {
                                    "Symbol":pair_symbol,
                                    "Type": pair_type,
                                    "name": pair_name,
                                    "Dividend": extract_yield(pair.get("eq_dividend_yield"))
                                }
                                if pair_info["name"]:
                                    df_list.append(pair_info)
    if df_list:
        df = pd.DataFrame(df_list)
        df.set_index('name', inplace=True)
        return df
    return pd.DataFrame()

def get_additional_fields(stock_ids):
    if not stock_ids:
        return None

    if isinstance(stock_ids, int):
        stock_ids = [str(stock_ids)]
    elif isinstance(stock_ids, str):
        stock_ids = [stock_ids]

    results = {}
    for stock_id in stock_ids:
        try:
            result = get_infos(stock_id)
            if result:
                results[stock_id] = result
        except Exception as exc:
            # Silently continue processing other stocks
            continue
    
    if not results:
        raise ValueError("No data fetched, check the stock IDs or API response")

    # Reconstruct the DataFrame in the order of stock_ids
    ordered_results = [results[stock_id] for stock_id in stock_ids if stock_id in results]
    
    df = extract_data(ordered_results)

    if df.empty:
        raise ValueError("Failed to convert data to DataFrame")

    return df