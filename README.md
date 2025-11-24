# Video Game Sales Business Intelligence Analysis

> Graduate-level BI project analyzing historical video game sales to guide development strategy and market positioning.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![PowerBI](https://img.shields.io/badge/analytics-Power_BI-yellow.svg)
![BI](https://img.shields.io/badge/BI-OLAP_Analysis-orange.svg)
![SQLite](https://img.shields.io/badge/database-SQLite-green.svg)
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
uv run python src/analytics_project/data_prep.py
uv run python src/analytics_project/etl_to_dw.py
# Open reports/video_game_sales.pbix in Power BI Desktop
```

## 📊 Project Overview

This BI project analyzes historical video game sales data to provide strategic insights for game development studios, focusing on genre performance, platform targeting, and publisher partnerships.

---

## 🎯 Current Status: DATA PIPELINE COMPLETE ✅

**Data Processing Pipeline**: ✅ **Fully Implemented and Tested**

### ✅ Completed Work:

1. **Data Preparation Script** (`src/analytics_project/data_prep.py`)
   - Loads raw vgsales.csv from Kaggle
   - Handles missing values and data validation
   - Creates derived features (decades, success categories, regional percentages)
   - Exports cleaned data to `data/prepared/vgsales_cleaned.csv`

2. **Data Warehouse ETL** (`src/analytics_project/etl_to_dw.py`) 
   - Implements star schema in SQLite database
   - Creates dimension tables: platform_dim, genre_dim, publisher_dim, time_dim, game_dim
   - Creates fact table: game_sales_fact with sales metrics
   - Builds proper indexes and relationships for OLAP operations
   - Output: `data/dw/video_games_dw.sqlite`

### 🎯 Ready for Next Phase:
- **Power BI Dashboard Development** - Connect to SQLite database and build interactive visuals
- **OLAP Analysis Implementation** - Slicing, dicing, drilldown operations
- **Business Insights Generation** - Strategic recommendations based on data patterns

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
- **SQLite**: Star schema data warehouse storage
- **GitHub Actions**: Automated documentation deployment
- **MkDocs**: Project documentation site

## 4. Workflow & Logic

### Data Pipeline Architecture:

```
Raw Data (vgsales.csv) 
    → Data Preparation (data_prep.py)
    → Cleaned Data (vgsales_cleaned.csv) 
    → Data Warehouse ETL (etl_to_dw.py)
    → SQLite Star Schema (video_games_dw.sqlite)
    → Power BI Dashboard
```

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
1. **Data Preparation**: Clean and validate raw game sales data ✅
2. **Star Schema**: Implement data warehouse with fact and dimension tables ✅
3. **Power BI Modeling**: Create relationships and calculated measures 🚧
4. **Visual Exploration**: Interactive analysis using OLAP operations 🚧
5. **Insight Generation**: Identify patterns and strategic opportunities 🚧

## 5. Data Warehouse Schema

### Star Schema Design:

```
game_sales_fact (Fact Table)
  │
  ├── platform_dim (Platform details)
  ├── genre_dim (Game genres) 
  ├── publisher_dim (Publisher information)
  ├── time_dim (Time periods with decades/eras)
  └── game_dim (Game attributes and metadata)
```

### Key Tables:
- **game_sales_fact**: Sales metrics with foreign keys to all dimensions
- **platform_dim**: Gaming platforms (PS, Xbox, Nintendo, etc.)
- **genre_dim**: Game genres (Action, RPG, Sports, etc.)
- **publisher_dim**: Publishers (Nintendo, EA, Activision, etc.)
- **time_dim**: Time analysis with decade and era groupings
- **game_dim**: Game details and success categories

## 6. Power BI Connection Guide

### Direct SQLite Connection (Recommended):

```
1. Open Power BI Desktop
2. Get Data → More... → Other → SQLite database
3. Navigate to: data/dw/video_games_dw.sqlite
4. Select all dimension and fact tables
5. Create relationships:
   - game_sales_fact[platform_id] → platform_dim[platform_id]
   - game_sales_fact[genre_id] → genre_dim[genre_id]
   - game_sales_fact[publisher_id] → publisher_dim[publisher_id]
   - game_sales_fact[time_id] → time_dim[time_id]
```

## 7. Expected Results

### Key Findings (Based on Initial Analysis)

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

### Visualizations Planned

- **Stacked Bar Charts**: Regional sales breakdown by genre
- **Line Charts**: Platform sales trends over time
- **Matrix Heat Maps**: Publisher performance across platforms
- **Treemaps**: Market share visualization by publisher
- **Scatter Plots**: Sales volume vs. release year analysis

## 8. Current File Structure

```
bi-video-game-sales-analysis/
├── data/
│   ├── raw/
│   │   └── vgsales.csv                 # Original Kaggle dataset
│   ├── prepared/
│   │   └── vgsales_cleaned.csv         # Cleaned data from data_prep.py ✅
│   └── dw/
│       └── video_games_dw.sqlite       # SQLite data warehouse ✅
├── src/
│   └── analytics_project/
│       ├── data_prep.py               # Data preparation script ✅
│       ├── etl_to_dw.py               # Data warehouse ETL ✅
│       └── utils_logger.py            # Logging configuration
├── reports/
│   └── video_game_sales.pbix          # Power BI dashboard 🚧
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
uv run python src/analytics_project/data_prep.py

# Build data warehouse
uv run python src/analytics_project/etl_to_dw.py
```

### 3.2 Power BI Analysis
1. Open `reports/video_game_sales.pbix` in Power BI Desktop
2. Connect to `data/dw/video_games_dw.sqlite` using SQLite connector
3. Create relationships between fact and dimension tables
4. Build OLAP operations:
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
- Use direct SQLite file connection (not DSN)

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

- [x] Complete data validation and quality checks ✅
- [x] Build data preparation pipeline ✅  
- [x] Implement star schema data warehouse ✅
- [ ] Build initial Power BI dashboard with core visuals 🚧
- [ ] Implement advanced OLAP operations 🚧
- [ ] Create business insight documentation 🚧
- [ ] Deploy project documentation site 🚧

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Kaggle for the Video Game Sales dataset
- Power BI community for OLAP operation guidance
- Graduate program instructors for project framework

---

*Last updated: November 24, 2025*
*Status: Data Pipeline Complete - Ready for Power BI Development*