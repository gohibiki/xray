# Contributing to Investment Portfolio Manager

Thank you for your interest in contributing to the Investment Portfolio Manager! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs. actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages or logs**
- **Screenshots** if applicable

Use the [issue template](.github/ISSUE_TEMPLATE.md) when reporting bugs.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear use case** describing why this enhancement would be useful
- **Detailed description** of the proposed functionality
- **Possible implementation** approach (optional)
- **Alternative solutions** you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes** thoroughly:
   - Test with various portfolio configurations
   - Verify optimization algorithms still work
   - Check PDF generation
   - Test on different operating systems if possible

4. **Update documentation** as needed:
   - Update README.md if adding features
   - Add/update code comments
   - Create/update relevant .md files

5. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request** using the [PR template](.github/PULL_REQUEST_TEMPLATE.md)

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Code Organization

- Keep related functionality in appropriate modules
- Maintain separation of concerns
- Use helper functions to avoid code duplication
- Add comments for complex logic

### Example Code Style

```python
def calculate_portfolio_metrics(prices_df, weights):
    """
    Calculate comprehensive portfolio metrics.

    Args:
        prices_df (pd.DataFrame): Historical price data
        weights (list): Portfolio weights

    Returns:
        pd.DataFrame: Calculated metrics
    """
    # Calculate returns
    returns = prices_df.pct_change()

    # Apply weights and calculate metrics
    portfolio_returns = returns.dot(weights)

    return metrics_df
```

### Cross-Platform Compatibility

- **Always use `os.path.join()`** for file paths
- Never use hardcoded paths like `/files/` or `C:\files\`
- Test on both Windows and Unix-like systems if possible

```python
# Good
file_path = os.path.join(os.path.dirname(__file__), "data", "file.csv")

# Bad
file_path = "/data/file.csv"
```

### Error Handling

- Provide informative error messages
- Catch specific exceptions when possible
- Include context in error messages

```python
try:
    result = calculate_optimization(data)
except ValueError as e:
    st.error(f"Optimization failed: {str(e)}. Please ensure you have at least 2 holdings with sufficient historical data.")
```

## Development Setup

1. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/xray.git
   cd xray
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit secrets.toml with your API keys
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, test the following:

- [ ] Application starts without errors
- [ ] Search functionality works
- [ ] Portfolio save/load/delete works
- [ ] All 4 main tabs render correctly
- [ ] Optimization algorithms produce results
- [ ] PDF generation works
- [ ] Error messages are helpful
- [ ] No console errors or warnings

### Test Cases to Consider

1. **Edge Cases**:
   - Empty portfolios
   - Single holding
   - Invalid weight combinations
   - Missing data

2. **Special Securities**:
   - Test KMLM (pair_ID 1196641)
   - Test TFLO (pair_ID 1191927)
   - Test securities with limited history

3. **Cross-Platform**:
   - Test file paths work on both Windows and Unix
   - Verify PDF generation on different systems

## Project Structure

```
xray/
├── app.py                  # Main application
├── additional_info.py      # Security data fetching
├── holdings.py            # Portfolio holdings
├── layout.py              # CSS styling
├── metrics.py             # Performance calculations
├── optimizations.py       # Optimization algorithms
├── search.py              # Search functionality
├── xray.py                # PDF generation
└── requirements.txt       # Dependencies
```

### Module Responsibilities

- **app.py**: Main Streamlit app, UI components, workflow orchestration
- **additional_info.py**: Fetch additional security metadata
- **holdings.py**: Process and aggregate portfolio holdings
- **layout.py**: Custom CSS and styling
- **metrics.py**: Calculate performance metrics
- **optimizations.py**: Portfolio optimization algorithms
- **search.py**: Security search functionality
- **xray.py**: PDF report generation

## Financial Calculations

When modifying financial calculations:

- **Document the methodology** in code comments
- **Verify against known benchmarks** when possible
- **Consider edge cases** (negative returns, zero volatility, etc.)
- **Maintain consistency** with industry standards

## Documentation

### Code Comments

Add comments for:
- Complex algorithms
- Financial formulas
- Non-obvious logic
- Hardcoded values (with explanations)
- Special cases or workarounds

### README Updates

Update README.md when:
- Adding new features
- Changing dependencies
- Modifying setup steps
- Adding new configuration options

## Questions or Need Help?

- **Check existing issues** for similar questions
- **Create a new issue** with the "Question" label
- **Provide context** about what you're trying to accomplish

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in the project. Thank you for helping improve the Investment Portfolio Manager!
