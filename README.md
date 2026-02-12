# Investment Portfolio Manager

A sophisticated web application for investment portfolio analysis, optimization, and reporting built with Streamlit. This tool provides comprehensive portfolio analytics including risk assessment, performance tracking, and professional PDF reporting capabilities.

## Live Demo

[🚀 View Live Application](your-streamlit-deployment-url-here)

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
- **Portfolio Persistence**: Save and load multiple portfolio configurations
- **Real-time Data**: Integration with Investing.com and Financial Modeling Prep APIs
- **Interactive Search**: Auto-complete search for thousands of ETFs, funds, and securities
- **Data Validation**: Comprehensive input validation and error handling

## Technology Stack

### Core Framework
- **Frontend**: Streamlit 1.26.0
- **Data Processing**: Pandas 2.2.1, NumPy 1.23.5

### Financial Analytics
- **Optimization**: PyPortfolioOpt 1.5.5 (Mean-Variance, HRP, CLA)
- **Data Sources**: InvestGo 1.0.2, Financial Modeling Prep API
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
- Financial Modeling Prep API key (free tier available)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/investment-portfolio-manager.git
cd investment-portfolio-manager
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

4. Configure API credentials:
Create `.streamlit/secrets.toml`:
```toml
[api_keys]
financial_modeling_prep = "your_api_key_here"
```

5. Run the application:
```bash
streamlit run app.py
```

### Getting API Keys

**Financial Modeling Prep** (Required for dividend data):
1. Visit [financialmodelingprep.com](https://financialmodelingprep.com/)
2. Sign up for free account (250 requests/day)
3. Copy your API key to `.streamlit/secrets.toml`

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

3. **Save Portfolio**:
   - Enter a portfolio name
   - Click the save button (💾)
   - Access saved portfolios via dropdown

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

## API Dependencies

### Required APIs
- **Financial Modeling Prep**: Dividend data retrieval
- **Investing.com**: Price data and search functionality (via InvestGo)

### Rate Limits
- Financial Modeling Prep: 250 requests/day (free tier)
- Application implements 24-hour caching to minimize API calls

## Project Structure

```
investment-portfolio-manager/
├── app.py                 # Main Streamlit application
├── additional_info.py     # Security data fetching and processing
├── holdings.py           # Portfolio holdings aggregation
├── layout.py             # Custom CSS styling
├── metrics.py            # Performance calculations
├── optimizations.py      # Portfolio optimization algorithms
├── search.py             # Security search functionality
├── xray.py               # PDF report generation
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── secrets.toml      # API configuration (not in repo)
└── .gitignore           # Git ignore rules
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
- **Persistent**: Saved portfolio configurations

### Data Processing
- **Parallel Processing**: Multi-threaded API requests where applicable
- **Interpolation**: Missing data points handled via forward/backward fill
- **Outlier Detection**: Statistical filtering for data quality

## Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in the Streamlit Cloud dashboard:
   ```toml
   [api_keys]
   financial_modeling_prep = "your_api_key_here"
   ```

### Local Development

```bash
# Run with custom port
streamlit run app.py --server.port 8502

# Enable debug mode
streamlit run app.py --logger.level debug
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (if implemented)
python -m pytest tests/

# Format code
black *.py

# Lint code
flake8 *.py
```

## Disclaimer

This application is for educational and informational purposes only. It should not be considered as investment advice. Always consult with qualified financial professionals before making investment decisions. Past performance does not guarantee future results.

**Risk Warning**: All investments carry risk of capital loss. The value of investments and any income from them can go down as well as up.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Author**: [gohibiki]  
**Email**: [gohibiki@protonmail.com]
**GitHub**: [[gohibiki](https://github.com/gohibiki)]

## Acknowledgments

- **PyPortfolioOpt** for optimization algorithms
- **Streamlit** for the web framework
- **Financial Modeling Prep** for market data
- **Investing.com** for comprehensive financial data

---

**Built with Python, Streamlit, and modern portfolio theory principles.**