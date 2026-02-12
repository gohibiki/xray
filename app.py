import streamlit as st
import pandas as pd
import numpy as np
from streamlit_searchbox import st_searchbox
from layout import apply_custom_css
from search import fetch_search_results
from holdings import process_and_combine_holdings
from optimizations import optimize
from metrics import calculate_metrics
from additional_info import get_additional_fields
from xray import create_pdf
import investgo as go
from datetime import datetime, timedelta
import yfinance as yf
from streamlit_pdf_viewer import pdf_viewer
from streamlit_option_menu import option_menu
import os
import requests

# Page configuration
def set_page_config():
    st.set_page_config(page_title="Investment Portfolio Manager", layout="wide")
    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Historical Prices", "Optimisations", "Allocations", "Portfolio Report"],
        icons=["graph-up-arrow", "speedometer", "bar-chart-line", "file-earmark-bar-graph", "star"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={"container": {"padding": "0!important", "margin-top": "0rem"}})
    apply_custom_css()
    return selected

# Process selected ISINs
def process_isins(isin_list):
    return [
        st.session_state.get(f"suggestions_search_box_{i}", {}).get(isin)
        for i, isin in enumerate(isin_list) if isin
    ]

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_dividends(ticker):
    try:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends
        if not dividends.empty:
            dividends.index = dividends.index.tz_localize(None)
            return dividends.sort_index()
        return pd.Series()
    except Exception as e:
        st.error(f"Error fetching dividend data: {str(e)}")
        return pd.Series()

def adjust_prices_for_dividends(df_stock, dividends):
    dividends.index = dividends.index.tz_localize(None)
    dividends = dividends.reindex(df_stock.index, fill_value=0)
    return df_stock.add(dividends.cumsum(), axis=0)

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_historical_prices(pair_id, start, end):
    df_stock = go.get_historical_prices(pair_id, start, end).price
    df_stock.index = pd.to_datetime(df_stock.index, format='%d%m%Y')
    
    # Special data cleaning for pair_ID 45429 (specific ETF with known data quality issues)
    # Apply more aggressive outlier detection using multiple statistical methods
    if pair_id == 45429:
        # Store original values for comparison
        original_values = df_stock.copy()
        
        # First pass: Remove extreme values using z-score
        z_scores = (df_stock - df_stock.mean()) / df_stock.std()
        mask_zscore = np.abs(z_scores) <= 3  # Increased from 0.8
        
        # Second pass: Remove large price changes using percentage difference from median
        price_diff_from_median = np.abs(df_stock - df_stock.median()) / df_stock.median()
        mask_median = price_diff_from_median <= 0.5  # Increased from 0.2
        
        # Third pass: Remove consecutive high values
        rolling_median = df_stock.rolling(window=5, center=True).median()
        mask_rolling = np.abs(df_stock - rolling_median) / rolling_median <= 0.55  # Increased from 0.15
        
        # Combine all filters
        final_mask = mask_zscore & mask_median & mask_rolling
        df_stock_filtered = df_stock[final_mask]
    else:
        z_scores = (df_stock - df_stock.mean()) / df_stock.std()
        df_stock_filtered = df_stock[np.abs(z_scores) <= 2.5]
    
    return df_stock_filtered

def convert_daily_returns_to_prices(daily_returns_df, initial_price):
    daily_returns_df['Date'] = pd.to_datetime(daily_returns_df['Date'])
    daily_returns_df = daily_returns_df.set_index('Date')
    daily_returns_df['Price'] = initial_price * (1 + daily_returns_df['Daily Return']).cumprod()
    return daily_returns_df[['Price']]

@st.cache_data(ttl=86400, show_spinner=False)
def load_datas(selected_isins, additional_info_df, adjust_for_dividends=True):
    dfs, col_names = [], []
    start, end = (datetime.today() - timedelta(days=5*365)).strftime('%d%m%Y'), datetime.today().strftime('%d%m%Y')

    for selected in selected_isins:
        if selected:
            pair_id, stock_name = selected["pair_ID"], selected["search_main_longtext"]
            
            # Special handling for KMLM (pair_ID 1196641)
            # This ETF requires combining scraped data with CSV historical returns
            if pair_id == 1196641:  # KMLM
                # Download data within the date range
                df_stock = fetch_historical_prices(1196641, start, end)
                df_stock = df_stock.to_frame(name=f'{stock_name}_scraped')
                df_stock.index = pd.to_datetime(df_stock.index)
                
                # Get the initial price from the downloaded data
                initial_price = df_stock.iloc[0, 0]
                
                # Load CSV data and convert daily returns to prices
                # KMLM data file contains historical daily returns for this specific ETF
                csv_path = os.path.join(os.path.dirname(__file__), "KMLM.csv")
                daily_data = pd.read_csv(csv_path, parse_dates=['Date'])
                daily_prices_df = convert_daily_returns_to_prices(daily_data, initial_price)
                
                # Merge Yahoo Finance data and CSV data
                combined_df = pd.merge(df_stock, daily_prices_df, left_index=True, right_index=True, how='outer', suffixes=('_scraped', '_from_csv'))
            
                if f'{stock_name}_scraped' in combined_df.columns and 'Price' in combined_df.columns:
                    combined_df.loc[:, f'{stock_name}_scraped'] = combined_df[f'{stock_name}_scraped'].fillna(combined_df['Price'])
            
                combined_df.drop(columns=['Price'], inplace=True)
            
                # Convert 'start' and 'end' back to datetime for comparison
                start_dt = datetime.strptime(start, '%d%m%Y')
                end_dt = datetime.strptime(end, '%d%m%Y')
            
                # Filter combined_df within the selected date range
                combined_df = combined_df[(combined_df.index >= start_dt) & (combined_df.index <= end_dt)]
                combined_df = combined_df.loc[~combined_df.index.duplicated(keep='first')]
                df_stock = combined_df
                
            # TFLO (pair_ID 1191927) uses alternative data source (pair_ID 959362)
            elif pair_id == 1191927:  # TFLO
                df_stock = fetch_historical_prices(959362, start, end)
            else:
                df_stock = fetch_historical_prices(pair_id, start, end)

            if adjust_for_dividends and stock_name in additional_info_df.index:
                ticker = additional_info_df.loc[stock_name, "Symbol"]
                dividends = fetch_dividends(ticker)
                if not dividends.empty:
                    df_stock = adjust_prices_for_dividends(df_stock, dividends)

            dfs.append(df_stock)
            col_names.append(stock_name)

    if dfs:
        combined_df = pd.concat(dfs, axis=1)
        combined_df.columns = col_names
        return combined_df.interpolate().ffill().bfill().dropna()

@st.cache_data(ttl=86400, show_spinner=False)
def get_additional_fields_cached(pair_ids):
    return get_additional_fields(pair_ids)

# Display functions
@st.fragment
def display_prices(combined_df):
    df_resampled = (1 + combined_df.pct_change()).cumprod().resample('W').mean()
    st.line_chart(df_resampled, height=650)

@st.fragment
def display_correlation(combined_df):
    correlation_df = combined_df.pct_change().corr(method='spearman')
    mask = np.triu(np.ones_like(correlation_df, dtype=bool), k=1)
    sorted_pairs = correlation_df.where(mask).unstack().dropna().sort_values(ascending=False).head(5)
    st.dataframe(sorted_pairs)

# Load data and display
@st.fragment
def load_data_and_display(selected_isins):
    additional_info_df = get_additional_fields_cached([isin["pair_ID"] for isin in selected_isins if isin])
    combined_df = load_datas(selected_isins, additional_info_df)
    
    if combined_df is not None:
        metrics_df = calculate_metrics(combined_df)
        combined_metrics_df = pd.concat([additional_info_df, metrics_df], axis=1)
        st.subheader("Metrics", anchor=False)
        st.dataframe(combined_metrics_df, use_container_width=True)
        st.subheader("Historical Prices", anchor=False)
        display_prices(combined_df)
        st.subheader("Correlations", anchor=False)
        display_correlation(combined_df)

# Optimize and display
@st.fragment
def optimize_and_display(selected_isins, weight_list):
    additional_info_df = get_additional_fields_cached(
        [isin["pair_ID"] for isin in selected_isins if isin]
    )
    df_stocks = load_datas(selected_isins, additional_info_df)
    weights_df = optimize(df_stocks)

    if any(weight_list):
        manual_weights = [float(item)/100 for item in weight_list if item]
        weights_df['Manual'] = manual_weights

    returns = df_stocks.pct_change()
    metrics_df = calculate_metrics(df_stocks, returns, weights_df)

    st.subheader("Portfolio Weights (%)", anchor=False)
    st.dataframe((weights_df * 100).style.format("{:.2f}"), use_container_width=True)

    st.subheader("Performance Metrics", anchor=False)
    st.dataframe(metrics_df.T, use_container_width=True)

    st.subheader("Cumulative Returns Comparison", anchor=False)
    plot_optimize = pd.concat(
        [(1 + returns.dot(weights_df[col])).cumprod() for col in weights_df.columns],
        axis=1
    )
    plot_optimize.columns = weights_df.columns
    st.line_chart(plot_optimize.resample('W').last(), height=650)


# Generate X-Ray report
@st.fragment
def generate_xray_report(selected_isins, investment_strategy, weight_list, sri_value, selected_lines, benchmark_id=None):
    selected_ids = [isin["pair_ID"] for isin in selected_isins if isin]
    if not selected_ids:
        st.error("Select at least one holding.")
        return

    additional_info_df = get_additional_fields_cached(selected_ids)
    combined_df = load_datas(selected_isins, additional_info_df, adjust_for_dividends=True)

    if combined_df is not None:
        metrics_df = calculate_metrics(combined_df)
        combined_metrics_df = pd.concat([additional_info_df, metrics_df], axis=1).reset_index()

        str_length = 30 if selected_lines == "One Line" else 66
        combined_metrics_df.iloc[:, 0] = combined_metrics_df.iloc[:, 0].apply(lambda x: x[:str_length] if isinstance(x, str) else x)
        combined_metrics_df = combined_metrics_df.rename(columns={'Dividend': 'Yield'})
        combined_metrics_df = combined_metrics_df.map(lambda x: x.replace("Consumer Defensive", "Consumer Def.") if isinstance(x, str) else x)
        combined_metrics_df = combined_metrics_df.map(lambda x: x.replace("Communication Services", "Comm. Serv.") if isinstance(x, str) else x)
        combined_metrics_df = combined_metrics_df.map(lambda x: x.replace("Consumer Cycle", "Consumer Cyc.") if isinstance(x, str) else x)
        combined_metrics_df.drop(columns=['Symbol', 'Vol.', 'Type'], inplace=True)
        combined_metrics_df.columns = [""] + combined_metrics_df.columns[1:].tolist()
        columns = list(combined_metrics_df.columns)
        columns.insert(1, columns.pop(columns.index('Yield')))
        combined_metrics_df = combined_metrics_df[columns]

        port_weight = [item for item in weight_list if item]

        if port_weight:
            if len(port_weight) == len(combined_df.columns) and sum(float(item) for item in port_weight if item) == 100.0:
                weights = [float(item) / 100 for item in port_weight]
            elif len(port_weight) == 1 and float(port_weight[0]) == 100.0:
                weights = [1.0]
            else:
                st.warning('Missing Weight, Equal Weight Applied')
                weights = [1 / len(combined_df.columns)] * len(combined_df.columns)
        else:
            st.warning('No Weights Provided, Equal Weight Applied')
            weights = [1 / len(combined_df.columns)] * len(combined_df.columns)

        column_name = combined_metrics_df.columns[0]
        combined_metrics_df[column_name] = [f"{w*100:.0f}% {ticker}" for w, ticker in zip(weights, combined_metrics_df[column_name])]

        additional_info_df['Dividend'] = additional_info_df['Dividend'].replace('-', '0').str.rstrip('%').astype(float) / 100
        weighted_dividends = (additional_info_df['Dividend'].fillna(0) * weights).sum() * 100

        cumulative_returns = (1 + combined_df.pct_change().dropna()).cumprod()
        portfolio = (cumulative_returns * weights).sum(axis=1)
        portfolio_metrics = calculate_metrics(prices_df=combined_df,returns_df=combined_df.pct_change().iloc[1:],weights_df=pd.DataFrame(weights,index=combined_df.T.index)).reset_index()
        combined_portfolio = (1 + combined_df.pct_change().dot(weights)).cumprod().dropna()

        portfolio_metrics.columns = [""] + portfolio_metrics.columns[1:].tolist()
        portfolio_metrics['Yield'] = "{:.2f}%".format(weighted_dividends)

        # Default benchmark: MSCI World Index (pair_ID 38156)
        if benchmark_id is None:
            benchmark_id = "38156"

        benchmark_data = [{"pair_ID": benchmark_id, "search_main_longtext": "Benchmark"}]
        additional_info_bench = get_additional_fields_cached([benchmark_id])
        combined_bench = load_datas(benchmark_data, additional_info_bench, adjust_for_dividends=True)
        benchmark = combined_bench['Benchmark']
        combined_bench = (1 + benchmark.pct_change()).cumprod().dropna()

        benchmark_metrics = calculate_metrics(combined_bench.to_frame(name='Benchmark')).reset_index(drop=True)
        benchmark_dividends = additional_info_bench['Dividend'].replace('-', '0').str.rstrip('%').astype(float).fillna(0).sum() / 100
        benchmark_metrics['Yield'] = "{:.2f}%".format(benchmark_dividends * 100)
        bench_name = additional_info_bench.index.item()

        benchmark_row = {"": ["Benchmark"]}
        for col in portfolio_metrics.columns[1:]:
            benchmark_row[col] = [benchmark_metrics[col].iloc[0]] if col in benchmark_metrics.columns else [None]

        benchmark_row_df = pd.DataFrame(benchmark_row)
        portfolio_metrics = pd.concat([benchmark_row_df, portfolio_metrics], ignore_index=True)
        portfolio_metrics = portfolio_metrics.rename(columns={'Vol.': 'Volatility', 'Best Y': 'Best Year', 'Worst Y': 'Worst Year', '%/year': '5y Annualized'})
        columns = list(portfolio_metrics.columns)
        columns.insert(1, columns.pop(columns.index('Yield')))
        portfolio_metrics = portfolio_metrics[columns]
        portfolio_metrics.iloc[0, 0] = bench_name

        combined_sectors, combined_holdings = process_and_combine_holdings(selected_isins, weight_list)
        additional_data = {}
        if combined_sectors is not None and combined_holdings is not None:
            if len(combined_sectors) > 10:
                combined_sectors = pd.concat([combined_sectors.nlargest(9, 'val'),
                    pd.DataFrame({'fieldname': ['Others'], 'val': [round(combined_sectors.nsmallest(len(combined_sectors)-9, 'val')['val'].sum(), 2)]})])
                    
            for idx, col, name in [(1, 'fldname', 'Others'), (3, 'key', 'Others')]:
                small_sum = combined_holdings[idx][combined_holdings[idx]['val'] < 1]['val'].sum()
                combined_holdings[idx] = pd.concat([combined_holdings[idx][combined_holdings[idx]['val'] >= 1],
                    pd.DataFrame({col: [name], 'val': [round(small_sum, 2)]})]) if small_sum > 0 else combined_holdings[idx][combined_holdings[idx]['val'] >= 1]

            for i in range(len(combined_holdings)):
                combined_holdings[i] = combined_holdings[i].map(lambda x: x[:28] if isinstance(x, str) else x)

            additional_data = {
                'Asset Allocation': combined_holdings[1],
                'Country Exposure': combined_holdings[3],
                'Sector': combined_sectors,
                'Top Holdings': combined_holdings[0],
            }

        # Generate PDF in project root directory
        pdf_path = os.path.join(os.path.dirname(__file__), "portfolio_report.pdf")
        create_pdf(combined_metrics_df, combined_portfolio, portfolio_metrics, investment_strategy, sri_value, combined_bench, additional_data, benchmark)
        st.download_button(label="Download X-Ray PDF", data=open(pdf_path, "rb"), file_name="portfolio_report.pdf")
        pdf_viewer(pdf_path)

def main():
    selected = set_page_config()

    isin_col, main_col = st.columns([1, 5])

    with isin_col:
        isin_list, weight_list = [], []
        for i in range(10):
            col1, col2 = st.columns([4, 1])
            with col1:
                search_result = st_searchbox(
                    search_function=lambda query, key=f"search_box_{i}": fetch_search_results(query, key),
                    key=f"search_box_{i}",
                    placeholder=None,
                )
                isin_list.append(search_result)
            with col2:
                weight_key = f"weight_{i}"
                if weight_key not in st.session_state:
                    st.session_state[weight_key] = ""
                weight = st.text_input(f"weight_{i}", key=weight_key, label_visibility="collapsed")
                weight_list.append(weight)

        # Process ISINs and store in session state
        selected_isins = process_isins(isin_list)
        st.session_state.selected_isins = selected_isins
        st.session_state.weight_list = weight_list

    with main_col:
        # Content for each section
        if selected == "Historical Prices":
            load_data_and_display(st.session_state.get('selected_isins', []))

        elif selected == "Optimisations":
            st.subheader("Optimisations", anchor=False)
            try:
                optimize_and_display(st.session_state.get('selected_isins', []), st.session_state.get('weight_list', []))
            except (ValueError, IndexError, KeyError) as e:
                st.error(f'Select at least 2 holdings for optimization. Error: {str(e)}')
            except ImportError:
                # Handle missing pypfopt dependency
                st.error('PyPortfolioOpt library not found. Please install: pip install pyportfolioopt')
            except Exception as e:
                st.error(f'Optimization error: {str(e)}. Please check that you have selected valid holdings with sufficient historical data.')

        elif selected == "Allocations":
            st.subheader("Allocations", anchor=False)
            try:
                combined_sectors, combined_holdings = process_and_combine_holdings(st.session_state.get('selected_isins', []), st.session_state.get('weight_list', []))
                if combined_sectors is not None and combined_holdings is not None:
                    col1, col2, col3 = st.columns([1, 1, 1])

                    with col1:
                        st.subheader("Sector Allocation", anchor=False)
                        st.markdown(combined_sectors.to_html(index=False, header=False), unsafe_allow_html=True)

                    with col2:
                        st.subheader("Asset Allocation", anchor=False)
                        st.markdown(combined_holdings[1].to_html(index=False, header=False), unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.subheader("Country Exposure", anchor=False)
                        st.markdown(combined_holdings[3].to_html(index=False, header=False), unsafe_allow_html=True)

                    with col3:
                        st.subheader("Top Holdings", anchor=False)
                        st.markdown(combined_holdings[0].to_html(index=False, header=False), unsafe_allow_html=True)
                else:
                    st.write("Holdings information not available.")
            except (ValueError, IndexError, KeyError) as e:
                st.error(f'Select at least one holding to view allocations. Error: {str(e)}')
            except Exception as e:
                st.error(f'Error loading allocation data: {str(e)}. Ensure your holdings have sector and geographic data available.')

        elif selected == "Portfolio Report":
            benchmark_col, empty_col, preset_col = st.columns([2, 1.5, 3])

            with benchmark_col:
                st.subheader('Portfolio Report', anchor=False)
                benchmark_result = st_searchbox(
                    search_function=lambda query, key="benchmark_box": fetch_search_results(query, key),
                    key="benchmark_box",
                    placeholder="Choose a Benchmark (Default: MSCI World)",
                )
                benchmark_id = None
                if benchmark_result and "suggestions_benchmark_box" in st.session_state:
                    benchmark_info = st.session_state.get("suggestions_benchmark_box", {}).get(benchmark_result)
                    if benchmark_info:
                        benchmark_id = benchmark_info["pair_ID"]
                        st.write(f"Selected Benchmark ID: {benchmark_id}")

            with preset_col:
                line_options = ["One Line", "Two Lines"]
                selected_lines = st.selectbox("Display Format", line_options)
                sri_options = ["Default", "1", "2", "3", "4", "5", "6", "7"]
                selected_sri_option = st.selectbox("Overwrite Risk Indicator (SRI)", sri_options)
                sri_value = None if selected_sri_option == "Default" else int(selected_sri_option)

                preset_options = ["Defensive", "Balanced", "Aggressive", "Custom"]
                selected_preset = st.selectbox("Investment Strategy", preset_options)

                if selected_preset == "Custom":
                    custom_strategy = st.text_area("Write Your Custom Investment Strategy", "")
                else:
                    custom_strategy = {
                        "Defensive": "This Portfolio focuses on capital preservation and steady, risk-adjusted returns over the long term. The strategy emphasizes investments in high-quality bonds, blue-chip equities, and other low-volatility assets within stable industries. The portfolio is constructed with a strong focus on risk management and diversification to minimize potential drawdowns. The primary objective is to protect capital while generating consistent, modest returns.",
                        "Balanced": "This Portfolio seeks to achieve a harmonious blend of growth and income through a diversified approach to asset allocation. The strategy invests in a mix of equities and fixed income instruments across various sectors, aiming to capture upside potential while mitigating downside risks. The portfolio is designed to balance long-term capital appreciation with risk management, providing a stable investment experience with moderate volatility.",
                        "Aggressive": "The Portfolio targets maximum capital appreciation by focusing on high-growth opportunities in dynamic sectors such as technology and healthcare. The strategy involves a higher allocation to equities, including large-cap and international stocks, with a selective approach to high-yield fixed income instruments. The fund aims for substantial long-term gains, accepting higher volatility and risk as part of its pursuit of superior returns."
                    }[selected_preset]

            # Use the saved ISINs and weights in the Portfolio Report
            if 'selected_isins' in st.session_state and 'weight_list' in st.session_state:
                generate_xray_report(st.session_state.selected_isins, custom_strategy, st.session_state.weight_list, sri_value, selected_lines, benchmark_id)
            else:
                st.error("No ISINs and weights saved. Please save your selections first.")

if __name__ == "__main__":
    main()
