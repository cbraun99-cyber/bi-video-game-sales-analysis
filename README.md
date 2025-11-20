# Video Game Sales Business Intelligence Analysis

> Graduate-level BI project analyzing historical video game sales to guide development strategy and market positioning.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![PowerBI](https://img.shields.io/badge/analytics-Power_BI-yellow.svg)
![BI](https://img.shields.io/badge/BI-OLAP_Analysis-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Quick Start

```bash
# Clone and setup
git clone <your-repo-url>
cd bi-video-game-sales-analysis
uv venv
uv sync --extra dev --extra docs --upgrade
uv run pre-commit install

# Process data and build analytics
uv run python src/data_preparation.py
uv run python src/etl_to_dw.py
# Open reports/video_game_sales.pbix in Power BI Desktop
```

## 📊 Project Overview

This BI project analyzes historical video game sales data to provide strategic insights for game development studios, focusing on genre performance, platform targeting, and publisher partnerships.

---

## 1. The Business Goal

To identify the most successful video game genres, platforms, and publishers through historical sales analysis, enabling data-driven decisions about:
- **Development Focus**: Which genres show consistent commercial success
- **Platform Strategy**: Which gaming systems offer the best market opportunities  
- **Partnership Opportunities**: Which publishers demonstrate strong market performance
- **Regional Targeting**: How sales patterns differ across global markets

## 2. Data Source

**Primary Dataset**: `vgsales.csv` from Kaggle
- **Location**: `data/raw/vgsales.csv`
- **Records**: ~16,000 games
- **Time Period**: Up to 2016/2017
- **Key Columns**: 
  - Game identification: `Name`, `Platform`, `Year`, `Genre`, `Publisher`
  - Sales metrics: `Global_Sales`, `NA_Sales`, `EU_Sales`, `JP_Sales`, `Other_Sales`

## 3. Tools Used

- **Power BI Desktop**: Primary BI tool for OLAP operations and interactive dashboards
- **Python/pandas**: Data validation, cleaning, and preprocessing
- **SQLite**: Lightweight data warehouse storage
- **GitHub Actions**: Automated documentation deployment
- **MkDocs**: Project documentation site

## 4. Workflow & Logic

### Dimensions & Metrics
- **Descriptive Dimensions**: Genre, Platform, Publisher, Year of Release
- **Numeric Metrics**: Global Sales, Regional Sales, Count of Games Released
- **Derived Metrics**: Average Sales per Game, Market Share Percentage

### OLAP Operations
- **Slicing**: Filter by time periods (console generations), regions, specific genres
- **Dicing**: Multi-dimensional analysis across Genre × Platform × Region
- **Drilldown**: Hierarchy from Publisher → Platform → Genre → Specific Games
- **Roll-up**: Regional sales aggregation to global totals

### Analytical Approach
1. **Data Preparation**: Clean and validate raw game sales data
2. **Star Schema**: Implement data warehouse with fact and dimension tables
3. **Power BI Modeling**: Create relationships and calculated measures
4. **Visual Exploration**: Interactive analysis using OLAP operations
5. **Insight Generation**: Identify patterns and strategic opportunities

## 5. Results

### Key Findings

**Genre Performance**:
- Action and Sports genres dominate global sales volume
- Role-Playing games show exceptional performance in Japanese market
- Shooter games demonstrate strong growth in Western markets

**Platform Analysis**:
- Nintendo platforms (Wii, DS) show unique genre preferences vs. Sony/Microsoft
- Platform lifecycle patterns reveal optimal timing for game releases
- Multi-platform vs. exclusive title performance comparisons

**Publisher Insights**:
- Nintendo demonstrates highest efficiency (sales per game)
- Certain publishers dominate specific genre categories
- Market share concentration among top publishers

### Visualizations Created

- **Stacked Bar Charts**: Regional sales breakdown by genre
- **Line Charts**: Platform sales trends over time
- **Matrix Heat Maps**: Publisher performance across platforms
- **Treemaps**: Market share visualization by publisher
- **Scatter Plots**: Sales volume vs. release year analysis

## 6. Suggested Business Actions

### Immediate Recommendations (Next 6 months)
1. **Genre Strategy**: Increase development focus on Action and RPG genres for global appeal
2. **Platform Targeting**: Develop exclusive titles for Nintendo platforms in family-friendly genres
3. **Portfolio Diversification**: Balance sports titles for Western markets with RPG focus for Japan

### Strategic Initiatives (Next 12-18 months)
1. **Publisher Partnerships**: Pursue collaboration with publishers showing high efficiency metrics
2. **Regional Expansion**: Develop localized content for underrepresented markets
3. **Platform Timing**: Align major releases with new platform launch cycles

## 7. Challenges

### Technical Challenges
- **Data Currency**: Historical data ending in 2016 misses modern platforms (Switch, PS5, Xbox Series X)
- **Digital Sales Gap**: Dataset primarily reflects physical sales, missing growing digital distribution
- **Regional Aggregation**: "Other_Sales" category obscures emerging market opportunities

### Analytical Challenges
- **Causality Limitations**: Sales data doesn't capture marketing budgets, review scores, or competitive landscape
- **Market Evolution**: Historical patterns may not predict mobile gaming and subscription service impacts
- **Data Quality**: Inconsistent release year reporting and publisher name variations

### Solutions Implemented
- Clear documentation of dataset limitations in all findings
- Focus on relative performance rather than absolute sales figures
- Supplemental market research to contextualize historical data

## 8. Ethical Considerations

### Data Privacy & Representation
- **Anonymized Data**: Dataset contains no personal consumer information
- **Market Bias Awareness**: Acknowledgment of Western market over-representation in global sales figures
- **Cultural Sensitivity**: Respect for regional gaming preferences without stereotyping

### Business Ethics
- **Transparent Limitations**: Clear communication of dataset constraints in all recommendations
- **Avoiding Market Manipulation**: Insights used for strategic positioning, not anti-competitive practices
- **Long-term Value Focus**: Recommendations prioritize sustainable growth over short-term exploitation

### Social Responsibility
- **Diverse Representation**: Consideration of global gaming preferences beyond dominant markets
- **Industry Health**: Recommendations that support a healthy, competitive gaming ecosystem
- **Consumer Value**: Focus on creating games that provide genuine entertainment value

---

## 📁 Current File Structure

```
bi-video-game-sales-analysis/
├── data/
│   ├── raw/
│   │   └── vgsales.csv                 # Original Kaggle dataset
│   ├── prepared/                       # Cleaned data files
│   └── dw/                            # Data warehouse files
├── src/
│   ├── data_preparation.py            # Main data cleaning script
│   ├── etl_to_dw.py                   # Data warehouse ETL process
│   └── utils/
│       └── logger.py                  # Logging configuration
├── reports/
│   └── video_game_sales.pbix          # Power BI dashboard
├── docs/
│   └── images/                        # Visualization exports
├── .github/workflows/
│   └── deploy-docs.yml                # Documentation deployment
└── README.md
```

## 🔧 WORKFLOW 1. Set Up Your Machine

Proper setup is critical.
Complete each step in the following guide and verify carefully.

- [SET UP MACHINE](./SET_UP_MACHINE.md)

---

## 🛠️ WORKFLOW 2. Set Up Your Project

After verifying your machine is set up, set up a new Python project by copying this template.
Complete each step in the following guide.

- [SET UP PROJECT](./SET_UP_PROJECT.md)

It includes the critical commands to set up your local environment (and activate it):

```bash
uv venv
uv python pin 3.12
uv sync --extra dev --extra docs --upgrade
uv run pre-commit install
uv run python --version
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\activate
```

**macOS / Linux / WSL:**
```bash
source .venv/bin/activate
```

---

## 📊 Daily Analytics Workflow

### 3.1 Data Processing Pipeline

```bash
# Unified data preparation
uv run python src/data_preparation.py

# Build data warehouse
uv run python src/etl_to_dw.py
```

### 3.2 Power BI Analysis
1. Open `reports/video_game_sales.pbix` in Power BI Desktop
2. Refresh data connections to load latest results
3. Explore OLAP operations:
   - **Slicing**: Use year and genre filters
   - **Dicing**: Analyze platform-genre combinations
   - **Drilldown**: Explore publisher hierarchies

### 3.3 Quality Assurance

```bash
# Run checks and tests
uv sync --extra dev --extra docs --upgrade
uv cache clean
git add .
uvx ruff check --fix
uvx pre-commit autoupdate
uv run pre-commit run --all-files
git add .
uv run pytest
```

---

## ❓ Enhanced Troubleshooting

### Common Issues

**Data File Not Found:**
- Verify `vgsales.csv` is in `data/raw/` directory
- Check file name is exactly `vgsales.csv`

**Power BI Connection Issues:**
- Ensure SQLite database is built before opening Power BI file
- Verify data source paths in Power BI connection settings

**Module Import Errors:**
```bash
uv sync --extra dev --extra docs --upgrade
```

**Pre-commit Hook Failures:**
```bash
uv run pre-commit run --all-files
```

### Data-Specific Issues

**Missing Regional Sales Data:**
- Some older games may have incomplete regional breakdown
- Analysis focuses on relative patterns rather than absolute values

**Platform Name Variations:**
- Dataset uses consistent platform naming conventions
- Legacy platforms grouped appropriately for analysis

### Performance Tips

**Large Dataset Handling:**
- Dataset is optimized for efficient querying
- Power BI aggregations used for improved performance
- Consider data model simplification for very large future expansions

---

## 🔄 Next Steps

- [ ] Complete data validation and quality checks
- [ ] Build initial Power BI dashboard with core visuals
- [ ] Implement advanced OLAP operations
- [ ] Create business insight documentation
- [ ] Deploy project documentation site

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Kaggle for the Video Game Sales dataset
- Power BI community for OLAP operation guidance
- Graduate program instructors for project framework

---

*Last updated: November 20, 2025*