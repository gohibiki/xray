# Pre-Publish Checklist

Complete this checklist before publishing your repository to GitHub.

## ✅ Code Quality

- [x] All hardcoded file paths replaced with `os.path.join()`
- [x] Cross-platform compatibility verified
- [x] Error messages are descriptive and helpful
- [x] Code comments added for special cases
- [x] Trailing whitespace removed
- [x] No sensitive data (API keys, personal info) in code

## ✅ Documentation

- [x] README.md updated with accurate information
- [x] All placeholder URLs removed from README
- [x] Repository name updated (gohibiki/xray)
- [x] LICENSE file present (MIT)
- [x] CONTRIBUTING.md added
- [x] CHANGELOG.md created
- [x] KMLM_DATA_FORMAT.md documented
- [x] PORTFOLIO_FORMAT.md documented
- [x] Badges added to README
- [x] Contact information updated

## ✅ Configuration Files

- [x] requirements.txt has pinned versions
- [x] .gitignore properly configured
- [x] .streamlit/config.toml in place
- [x] .streamlit/secrets.toml.example created
- [x] files/.gitkeep added

## ✅ GitHub Setup

- [x] .github/ISSUE_TEMPLATE.md created
- [x] .github/PULL_REQUEST_TEMPLATE.md created

## 📋 Before First Commit

### 1. Review Sensitive Data
```bash
# Search for any API keys or secrets
grep -r "api_key" . --exclude-dir=.git --exclude-dir=__pycache__
grep -r "password" . --exclude-dir=.git --exclude-dir=__pycache__
grep -r "secret" . --exclude-dir=.git --exclude-dir=__pycache__
```

### 2. Test the Application
- [ ] Run `streamlit run app.py` successfully
- [ ] Test portfolio creation
- [ ] Test portfolio save/load
- [ ] Test all 4 tabs (Historical Prices, Optimizations, Allocations, Portfolio Report)
- [ ] Verify PDF generation works
- [ ] Test with different securities
- [ ] Check error messages are helpful

### 3. Verify File Structure
```bash
# Check all important files exist
ls -la .streamlit/secrets.toml.example
ls -la .github/ISSUE_TEMPLATE.md
ls -la files/.gitkeep
ls -la CONTRIBUTING.md
ls -la LICENSE
```

### 4. Clean Up
```bash
# Remove any test files
rm -f portfolio_report.pdf  # Will be regenerated
rm -f files/portfolios.json  # Will be regenerated

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
```

## 📤 Publishing to GitHub

### Initial Commit (if new repo)
```bash
git add .
git commit -m "Initial commit: Investment Portfolio Manager v1.0

Features:
- Portfolio analysis and optimization (8 strategies)
- Professional PDF reporting
- Real-time data integration
- Comprehensive metrics and analytics
- Cross-platform support"

git branch -M main
git remote add origin https://github.com/gohibiki/xray.git
git push -u origin main
```

### Update Existing Repo
```bash
git add .
git commit -m "Major update: Prepare for public release

Improvements:
- Fix cross-platform file paths
- Add comprehensive documentation
- Create GitHub templates
- Pin dependency versions
- Add code comments for clarity
- Improve error messages"

git push origin main
```

## 🚀 Post-Publish Tasks

### 1. Create a Release
- Go to GitHub → Releases → Create new release
- Tag: v1.0.0
- Title: "Investment Portfolio Manager v1.0.0"
- Description: Copy from CHANGELOG.md

### 2. Deploy to Streamlit Cloud (Optional)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select repository: gohibiki/xray
4. Set main file: app.py
5. Add secrets in dashboard:
   ```toml
   [api_keys]
   financial_modeling_prep = "your_key_here"
   ```
6. Deploy
7. Update README with live URL

### 3. Add Topics to GitHub Repo
Add these topics for discoverability:
- `portfolio-management`
- `portfolio-optimization`
- `streamlit`
- `finance`
- `python`
- `data-visualization`
- `investment-analysis`
- `modern-portfolio-theory`
- `financial-engineering`

### 4. Enable GitHub Features
- [ ] Enable Issues
- [ ] Enable Discussions (optional)
- [ ] Add repository description
- [ ] Add website URL (if deployed to Streamlit Cloud)

### 5. Social Media / CV
- [ ] Add to your LinkedIn projects
- [ ] Add to your portfolio website
- [ ] Tweet about it (if applicable)
- [ ] Add to your CV/resume

## 📊 Repository Settings

### Description
```
Sophisticated portfolio analysis, optimization & reporting tool built with Streamlit. Features 8 optimization strategies, professional PDF reports, and real-time financial data integration.
```

### Website
```
[Your Streamlit Cloud URL after deployment]
```

### Topics
```
portfolio-management, portfolio-optimization, streamlit, finance, python, investment-analysis
```

## 🔒 Security Checklist

- [x] No API keys in code
- [x] secrets.toml in .gitignore
- [x] No personal data in code
- [x] Example configuration files provided
- [ ] Consider adding SECURITY.md for vulnerability reporting

## 📝 Optional Enhancements

### Add Screenshots
1. Create `screenshots` directory
2. Take screenshots of:
   - Main dashboard
   - Historical prices chart
   - Optimization results
   - PDF report sample
3. Add to README.md

### Create Demo Video
1. Record 2-3 minute walkthrough
2. Upload to YouTube
3. Embed in README

### Add Unit Tests
```bash
# Create tests directory
mkdir tests
# Add test files
touch tests/test_metrics.py
touch tests/test_optimizations.py
```

## ✅ Final Verification

Before announcing your project:
- [ ] Repository is public
- [ ] README renders correctly on GitHub
- [ ] All links in README work
- [ ] LICENSE is visible
- [ ] Repository has description and topics
- [ ] Application runs without errors
- [ ] Documentation is clear and complete

## 🎉 Ready to Publish!

Once all checks are complete, your repository is ready for:
- Job applications
- Portfolio demonstrations
- Public use
- Contributions from others

Good luck with your project! 🚀
