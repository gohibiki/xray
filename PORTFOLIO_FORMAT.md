# Portfolio JSON Format

This document describes the format of saved portfolios in `files/portfolios.json`.

## File Location

The portfolio file is automatically created at:
- **Path**: `files/portfolios.json` (relative to project root)
- **Creation**: Auto-generated when you save your first portfolio
- **Backup**: Recommended to backup this file periodically

## JSON Structure

```json
{
  "Portfolio Name 1": {
    "isins": [
      {
        "pair_ID": 12345,
        "search_main_longtext": "Security Name 1",
        // ... other fields from search results
      },
      {
        "pair_ID": 67890,
        "search_main_longtext": "Security Name 2",
        // ... other fields from search results
      }
    ],
    "weights": ["40", "60"]
  },
  "Portfolio Name 2": {
    "isins": [...],
    "weights": [...]
  }
}
```

## Field Descriptions

### Portfolio Name (Key)
- **Type**: String
- **Description**: User-defined name for the portfolio
- **Constraints**: Must be unique within the file

### isins (Array)
- **Type**: Array of Objects
- **Description**: List of selected securities with their metadata
- **Source**: Data returned from the search API
- **Key Fields**:
  - `pair_ID`: Unique identifier for the security
  - `search_main_longtext`: Display name of the security
  - Additional fields vary based on security type

### weights (Array)
- **Type**: Array of Strings
- **Description**: Portfolio allocation percentages
- **Format**: String representation of percentage (e.g., "40" = 40%)
- **Constraints**:
  - Should sum to 100 for valid portfolios
  - Empty strings are allowed (will use equal weighting)
  - Must have same length as `isins` array

## Example Portfolio

```json
{
  "My Balanced Portfolio": {
    "isins": [
      {
        "pair_ID": 38156,
        "search_main_longtext": "MSCI World Index",
        "search_sub_text": "INDEX",
        "url": "/indices/msci-world"
      },
      {
        "pair_ID": 27866,
        "search_main_longtext": "Vanguard Total Bond Market ETF",
        "search_sub_text": "BND",
        "url": "/etfs/vanguard-total-bond-market-etf"
      }
    ],
    "weights": ["60", "40"]
  }
}
```

## Usage in Application

### Saving Portfolios
1. Enter holdings in the search boxes
2. Specify weights in the adjacent input fields
3. Enter a portfolio name
4. Click the save button (💾)

### Loading Portfolios
1. Select a portfolio from the dropdown menu
2. Holdings and weights are automatically populated
3. Modify as needed

### Deleting Portfolios
1. Select the portfolio from the dropdown
2. Keep the portfolio name in the text field
3. Click the delete button (☠️)

## File Management

### Manual Editing
- The JSON file can be manually edited with a text editor
- Ensure valid JSON syntax
- Backup before manual changes

### Backup Strategy
```bash
# Create a backup
cp files/portfolios.json files/portfolios.backup.json

# Restore from backup
cp files/portfolios.backup.json files/portfolios.json
```

### Migration
To transfer portfolios between installations:
1. Copy `files/portfolios.json` from old installation
2. Place in `files/` directory of new installation
3. Restart application

## Troubleshooting

### Empty Portfolio List
- Check if `files/portfolios.json` exists
- Verify JSON syntax is valid
- Ensure file permissions allow reading

### Portfolio Not Loading
- Verify `pair_ID` values are valid
- Check that security data is still available
- Try creating a new portfolio with fresh searches

### Weight Validation Issues
- Ensure weights are numeric strings
- Verify weights sum to 100
- Check array lengths match between isins and weights
