import pandas as pd
import investgo as go

def process_and_combine_holdings(selected_isins, weight_list):
    valid_entries = [(selected, float(weight_list[i]) / 100 if weight_list[i].strip() else 1 / len(selected_isins)) for i, selected in enumerate(selected_isins) if selected]
    
    combined_sectors = None
    combined_holdings = [None, None, None, None]
    
    for selected, weight in valid_entries:
        pair_id = selected["pair_ID"]
        #replace idsS
        if pair_id == 1024340: #xlps
            pair_id = 40690 #xlp
        holdings_info = go.get_holdings(pair_id)
        
        if len(holdings_info) >= 4:
            df_sectors = holdings_info[2].copy()
            df_sectors.iloc[:, 1] = df_sectors.iloc[:, 1].astype(float) * weight
            
            if combined_sectors is None:
                combined_sectors = df_sectors
            else:
                combined_sectors = pd.concat([combined_sectors, df_sectors], axis=0)
                combined_sectors = combined_sectors.groupby(combined_sectors.columns[0]).sum().reset_index()
            
            for i in range(4):
                df_copy = holdings_info[i].copy()
                df_copy.iloc[:, 1] = df_copy.iloc[:, 1].astype(float) * weight
                if combined_holdings[i] is None:
                    combined_holdings[i] = df_copy
                else:
                    combined_holdings[i] = pd.concat([combined_holdings[i], df_copy], axis=0)
                    combined_holdings[i] = combined_holdings[i].groupby(combined_holdings[i].columns[0]).sum().reset_index()

    combined_sectors.iloc[:, 1] = combined_sectors.iloc[:, 1].round(2)
    for i in range(4):
        combined_holdings[i].iloc[:, 1] = combined_holdings[i].iloc[:, 1].round(2)

    combined_sectors = combined_sectors.sort_values(by=combined_sectors.columns[1], ascending=False)
    combined_holdings[0] = combined_holdings[0].sort_values(by=combined_holdings[0].columns[1], ascending=False).head(10)
    combined_holdings[1] = combined_holdings[1].sort_values(by=combined_holdings[1].columns[1], ascending=False)
    combined_holdings[3] = combined_holdings[3].sort_values(by=combined_holdings[3].columns[1], ascending=False)
    
    return combined_sectors, combined_holdings