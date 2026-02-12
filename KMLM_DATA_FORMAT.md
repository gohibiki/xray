# KMLM.csv Data Format

This file contains historical daily returns data for the KMLM ETF (KFA Mount Lucas Managed Futures Index Strategy ETF).

## File Structure

The CSV file should have the following columns:

| Column Name   | Type   | Description                                      |
|---------------|--------|--------------------------------------------------|
| Date          | Date   | Trading date in format YYYY-MM-DD                |
| Daily Return  | Float  | Daily return as a decimal (e.g., 0.01 = 1%)     |

## Example

```csv
Date,Daily Return
2020-01-02,0.0023
2020-01-03,-0.0015
2020-01-06,0.0041
```

## Purpose

This data is used to supplement or replace scraped price data for the KMLM ETF (pair_ID 1196641). The application:
1. Fetches the initial price from the scraped data
2. Converts the daily returns to prices using the initial price
3. Merges the CSV-derived prices with scraped data
4. Fills missing scraped values with CSV-derived prices

## Usage in Code

See `app.py` lines 106-138 for the implementation of KMLM data loading and processing.

## Data Source

Historical daily returns can be obtained from:
- Financial data providers (Bloomberg, FactSet)
- ETF provider websites
- Financial APIs that provide total return data

## Notes

- Dates should be in chronological order
- Missing dates (weekends, holidays) should be omitted
- Daily returns should account for dividends and distributions
- The file is loaded relative to the application root directory
