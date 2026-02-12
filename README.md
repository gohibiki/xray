# Investment Portfolio Manager

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.26.0-FF4B4B.svg)](https://streamlit.io)
[![Portfolio Optimization](https://img.shields.io/badge/PyPortfolioOpt-1.5.6-green.svg)](https://pyportfolioopt.readthedocs.io/)

A sophisticated web application for investment portfolio analysis, optimization, and reporting built with Streamlit. This tool provides comprehensive portfolio analytics including risk assessment, performance tracking, and professional PDF reporting capabilities.

## 📊 Live Demo

> **Note:** Deploy to Streamlit Cloud and add your live URL here
>
> Instructions: Push to GitHub → Visit [share.streamlit.io](https://share.streamlit.io) → Connect repository

## Features

### Portfolio Analysis
- **Historical Performance Tracking**: 5-year lookback with customizable metrics (1m, 3m, YTD, 1yr, 3yr, 5yr)
- **Risk Metrics**: Volatility calculations and Synthetic Risk Indicator (SRI) assessment
- **Correlation Analysis**: Spearman correlation matrix for portfolio diversification insights
- **Dividend-Adjusted Returns**: Automatic dividend reinvestment calculations

### Portfolio Optimization
- **Multiple Optimization Strategies**:
  - Minimum Volatility (Mean-Variance & Exponentially Weighted)
  - Maximum Sharpe Ratio (Mean-Variance & Exponentially Weighted)
  - Hierarchical Risk Parity (HRP)
  - Critical Line Algorithm (CLA)
  - Equal Weight Baseline
- **Risk Models**: Ledoit-Wolf shrinkage estimator for robust covariance estimation
- **Custom Weight Support**: Manual portfolio weight specification and validation

### Professional Reporting
- **PDF Generation**: Comprehensive portfolio X-Ray reports with professional formatting
- **Allocation Analysis**: Sector, geographic, and asset class breakdowns
- **Benchmarking**: Compare against market indices (default: MSCI World)
- **Investment Strategy Documentation**: Built-in templates (Defensive, Balanced, Aggressive) or custom strategies

### Data Management
- **Real-time Data**: Integration with Investing.com (via InvestGo) and Yahoo Finance (via yfinance)
- **Interactive Search**: Auto-complete search for thousands of ETFs, funds, and securities
- **Data Validation**: Comprehensive input validation and error handling
- **No API Keys Required**: Uses free data sources

## Technology Stack

### Core Framework
- **Frontend**: Streamlit 1.26.0
- **Data Processing**: Pandas 2.2.1, NumPy

### Financial Analytics
- **Optimization**: PyPortfolioOpt 1.5.6 (Mean-Variance, HRP, CLA)
- **Data Sources**: InvestGo 1.0.2 (Investing.com), yfinance 0.2.37 (Yahoo Finance)
- **Risk Models**: Scikit-learn for statistical computations

### Visualization & Reporting
- **Charts**: Matplotlib, Streamlit native charting
- **PDF Reports**: ReportLab 4.2.0 with custom styling
- **UI Components**: Streamlit-searchbox, streamlit-option-menu

### Data Acquisition
- **Web Scraping**: CloudScraper, BeautifulSoup4 4.12.3
- **APIs**: Requests for HTTP client functionality

## Quick Start

### Prerequisites
- Python 3.8+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/gohibiki/xray.git
cd xray
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## Usage Guide

### Creating a Portfolio

1. **Search & Select Holdings**:
   - Use the search boxes in the left sidebar
   - Search by company name, ticker, or ISIN
   - Select up to 10 holdings per portfolio

2. **Set Portfolio Weights**:
   - Enter percentage weights (must sum to 100%)
   - Leave blank for equal weighting
   - Validation ensures proper weight allocation

### Analysis Features

**Historical Prices Tab**:
- View normalized performance charts
- Analyze key metrics table
- Examine correlation matrices

**Optimizations Tab**:
- Compare 8 different optimization strategies
- View optimized weights vs. manual allocation
- Analyze risk-adjusted returns

**Allocations Tab**:
- Sector exposure breakdown
- Geographic diversification
- Asset class allocation
- Top holdings analysis

**Portfolio Report Tab**:
- Generate professional PDF reports
- Customize investment strategy descriptions
- Override risk indicators
- Select benchmark comparisons

## Data Sources

### Free Data APIs (No API Keys Required)
- **Investing.com** (via InvestGo): Price data, search functionality, security metadata
- **Yahoo Finance** (via yfinance): Dividend data, historical prices

### Caching
- Application implements 24-hour caching to minimize API calls and improve performance
- All data sources are completely free with no rate limits or authentication required

## 📁 Project Structure

```
xray/
├── app.py                      # Main Streamlit application
├── additional_info.py          # Security data fetching and processing
├── holdings.py                 # Portfolio holdings aggregation
├── layout.py                   # Custom CSS styling
├── metrics.py                  # Performance calculations
├── optimizations.py            # Portfolio optimization algorithms
├── search.py                   # Security search functionality
├── xray.py                     # PDF report generation
├── requirements.txt            # Python dependencies
├── KMLM.csv                    # Historical data for KMLM ETF
├── GothamLight.ttf             # Font for PDF generation
├── OpenSans-VariableFont_*.ttf # Font for PDF generation
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── .github/
│   ├── ISSUE_TEMPLATE.md       # GitHub issue template
│   └── PULL_REQUEST_TEMPLATE.md # GitHub PR template
└── .gitignore                  # Git ignore rules
```

## Configuration

### Risk Model Parameters
- **Z-Score Threshold**: 3.0 (outlier detection)
- **Covariance Estimator**: Ledoit-Wolf shrinkage
- **Lookback Period**: 5 years (1,260 trading days)
- **Risk-Free Rate**: Automatically calculated from data

### Optimization Constraints
- **Maximum Holdings**: 10 per portfolio
- **Weight Bounds**: 0% to 100% per holding
- **Weight Sum**: Must equal 100%

## Performance Considerations

### Caching Strategy
- **24-hour TTL**: Price data, dividend data, security metadata
- **Session-based**: Search results, portfolio calculations

### Data Processing
- **Parallel Processing**: Multi-threaded API requests where applicable
- **Interpolation**: Missing data points handled via forward/backward fill
- **Outlier Detection**: Statistical filtering for data quality

## Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy (no secrets or API keys required!)

### Local Development

```bash
# Run with custom port
streamlit run app.py --server.port 8502

# Enable debug mode
streamlit run app.py --logger.level debug
```

## 🎯 Key Highlights

This project demonstrates:
- **Financial Engineering**: Implementation of Modern Portfolio Theory, multiple optimization algorithms (HRP, CLA, Mean-Variance), and risk models (Ledoit-Wolf shrinkage)
- **Data Engineering**: Real-time data integration from multiple sources, caching strategies, and data quality validation
- **Full-Stack Development**: Interactive web application with professional UI/UX
- **PDF Generation**: Custom report generation with professional formatting
- **API Integration**: Working with financial data APIs and web scraping
- **Python Best Practices**: Modular code architecture, error handling, cross-platform compatibility

## 📝 Technical Skills Demonstrated

- **Languages**: Python
- **Libraries**: Pandas, NumPy, SciPy, Scikit-learn, PyPortfolioOpt
- **Web Frameworks**: Streamlit
- **Data Visualization**: Matplotlib, Streamlit charts
- **APIs**: REST APIs (Investing.com via InvestGo, Yahoo Finance via yfinance)
- **Data Processing**: Time series analysis, statistical modeling, outlier detection
- **Report Generation**: ReportLab for PDF creation
- **Version Control**: Git, GitHub

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

This application is for educational and informational purposes only. It should not be considered as investment advice. Always consult with qualified financial professionals before making investment decisions. Past performance does not guarantee future results.

**Risk Warning**: All investments carry risk of capital loss. The value of investments and any income from them can go down as well as up.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Author**: gohibiki
**Email**: gohibiki@protonmail.com
**GitHub**: [github.com/gohibiki](https://github.com/gohibiki)
**LinkedIn**: [Add your LinkedIn profile here]

## Acknowledgments

- **PyPortfolioOpt** for optimization algorithms
- **Streamlit** for the web framework
- **Investing.com** for comprehensive financial data (via InvestGo)
- **Yahoo Finance** for dividend and price data (via yfinance)

---

**Built with Python, Streamlit, and modern portfolio theory principles.**