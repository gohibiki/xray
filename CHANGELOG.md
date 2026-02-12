# Changelog

All notable changes to the Investment Portfolio Manager project are documented in this file.

## [1.0.0] - 2025-02-12

### Added
- Initial release of Investment Portfolio Manager
- Portfolio analysis with historical performance tracking
- 8 portfolio optimization strategies (Min Vol, Max Sharpe, HRP, CLA, etc.)
- Professional PDF report generation with customizable investment strategies
- Real-time data integration with Investing.com (InvestGo) and Yahoo Finance (yfinance)
- Dividend-adjusted returns calculation
- Sector, geographic, and asset class allocation analysis
- Correlation analysis with Spearman method
- Customizable benchmark comparison (default: MSCI World Index)
- Synthetic Risk Indicator (SRI) calculation and override
- Interactive search with auto-complete for securities
- Support for up to 10 holdings per portfolio
- Cross-platform file path handling
- Comprehensive error messages and validation

### Documentation
- Added comprehensive README with installation instructions
- Created CONTRIBUTING.md with development guidelines
- Added KMLM_DATA_FORMAT.md for CSV data structure
- Created GitHub issue and PR templates

### Technical Features
- Streamlit 1.26.0 web framework
- PyPortfolioOpt 1.5.6 for optimization algorithms
- ReportLab 4.2.0 for PDF generation
- 24-hour data caching to minimize API calls
- Ledoit-Wolf shrinkage estimator for covariance
- Statistical outlier detection for data quality
- Exponentially weighted covariance matrices

### Known Limitations
- Maximum 10 holdings per portfolio
- 5-year historical lookback period
- PDF generation requires font files in project root
- Data dependent on Investing.com and Yahoo Finance availability

## Future Enhancements

### Planned Features
- [ ] Unit test coverage
- [ ] Automated backtesting functionality
- [ ] More benchmark options
- [ ] Export portfolio data to CSV/Excel
- [ ] Monte Carlo simulation for forward-looking projections
- [ ] Factor exposure analysis
- [ ] Transaction cost modeling
- [ ] Rebalancing recommendations
- [ ] Multi-currency support
- [ ] Dark mode UI theme

### Under Consideration
- [ ] Integration with additional data providers
- [ ] Support for crypto assets
- [ ] Mobile-responsive design improvements
- [ ] Collaboration features (portfolio sharing)
- [ ] Automated portfolio monitoring and alerts
- [ ] Integration with brokerage APIs

## Version History

- **1.0.0** (2025-02-12): Initial public release

---

For detailed changes and commits, see the [GitHub repository](https://github.com/gohibiki/xray).
