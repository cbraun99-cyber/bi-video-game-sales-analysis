# Video Game Sales Business Intelligence Analysis

> Graduate-level BI project analyzing historical video game sales to guide development strategy and market positioning.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![PowerBI](https://img.shields.io/badge/analytics-Power_BI-yellow.svg)
![BI](https://img.shields.io/badge/BI-OLAP_Analysis-orange.svg)
![SQL Server](https://img.shields.io/badge/database-SQL_Server-green.svg)
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
# Open data/dw/video_game_sales_analysis.pbix in Power BI Desktop
```

## 📊 Project Overview

This BI project analyzes historical video game sales data to provide strategic insights for game development studios, focusing on genre performance, platform targeting, and publisher partnerships.

---

## 🎯 Current Status: DATA WAREHOUSE & POWER BI FOUNDATION COMPLETE ✅

**Data Pipeline & Power BI Setup**: ✅ **Fully Implemented and Connected**

### ✅ Completed Work:

1. **Data Preparation Script** (`src/analytics_project/data_prep.py`)
   - Loads raw vgsales.csv from Kaggle
   - Handles missing values and data validation
   - Creates derived features (decades, success categories, regional percentages)
   - Exports cleaned data to `data/prepared/vgsales_cleaned.csv`

2. **SQL Server Data Warehouse ETL** (`src/analytics_project/etl_to_dw.py`) 
   - Implements star schema in SQL Server database
   - Creates dimension tables: platform_dim, genre_dim, publisher_dim, time_dim, game_dim
   - Creates fact table: game_sales_fact with sales metrics
   - Builds proper indexes and relationships for OLAP operations
   - Database: `VideoGamesDW` on SQL Server

3. **System DSN Configuration** 
   - DSN Name: `videogames`
   - Connected to SQL Server VideoGamesDW database
   - Tested and verified connection

4. **Power BI Foundation** (`data/dw/video_game_sales_analysis.pbix`)
   - ODBC connection to SQL Server via "videogames" DSN
   - Data model with star schema relationships established
   - Ready for dashboard development

🎯 **PROJECT COMPLETE: 3-Page Interactive Dashboard Delivered** ✅

### ✅ **Power BI Dashboard - Fully Implemented:**

**Page 1: Executive Summary**
- 4 KPI Cards: Total Global Sales ($8.58B), Total Games (15,540), Avg Sales Per Game ($0.55M), Top Genre (Action)
- Genre Market Share Donut Chart

**Page 2: Platform Analysis**  
- Platform KPIs: Platform Count (26), Top Selling Platform (PlayStation), Avg Sales Per Platform ($329.98M)
- Regional Sales Bubble Map with coordinate-based visualization
- Regional Sales Bar Chart

**Page 3: Platform Insights**
- Platform-Genre Performance Heatmap (Matrix with conditional formatting)
- Platform Sales Timeline (1980-2020) with multi-line trends
- Platform-Publisher Analysis (Stacked bar chart)

## 🎯 **Key Business Insights Discovered**

### **Genre Strategy:**
- **Action** dominates as top genre across all regions
- Consistent market share patterns globally

### **Platform Performance:**
- **PlayStation** leads as top-selling platform
- 26 distinct platforms analyzed with average $329.98M sales per platform

### **Regional Patterns:**
- Clear geographic sales distributions visible via bubble map
- Regional preferences identifiable through interactive filtering

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
- **SQL Server Express**: Database management system with ODBC connectivity
- **Python/pandas**: Data validation, cleaning, and preprocessing
- **GitHub Actions**: Automated documentation deployment
- **MkDocs**: Project documentation site

## 4. Workflow & Logic

### Data Pipeline Architecture:

```
Raw Data (vgsales.csv) 
    → Data Preparation (data_prep.py)
    → Cleaned Data (vgsales_cleaned.csv) 
    → SQL Server ETL (etl_to_dw.py)
    → SQL Server Database (VideoGamesDW)
    → System DSN (videogames)
    → Power BI Dashboard (video_game_sales_analysis.pbix)
```

### Dimensions & Metrics
- **Descriptive Dimensions**: Genre, Platform, Publisher, Year of Release
- **Numeric Metrics**: Global Sales, Regional Sales, Count of Games Released
- **Derived Metrics**: Average Sales per Game, Market Share Percentage

### **Completed OLAP Operations:**
- **Slicing**: Region filters (North America, Europe, Japan, Other)
- **Dicing**: Platform × Genre × Region multi-dimensional analysis
- **Drilldown**: Platform → Genre → Sales performance hierarchies
- **Roll-up**: Regional sales aggregation to global totals

### Analytical Approach
1. **Data Preparation**: Clean and validate raw game sales data ✅
2. **Star Schema**: Implement data warehouse with fact and dimension tables ✅
3. **Power BI Modeling**: Create relationships and calculated measures ✅
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

## 6. System DSN & Power BI Connection Guide

### SQL Server Express Installation

1. **Download SQL Server Express** from [Microsoft's website](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
2. **Run installer** with these settings:
   - Feature Selection: Database Engine Services
   - Instance Configuration: Default instance (or named instance like `SQLEXPRESS`)
   - Authentication Mode: Mixed Mode (set a strong 'sa' password)

### System DSN Setup

1. **Open ODBC Data Source Administrator** (64-bit):
   - Press `Windows Key + R`, type `odbcad32.exe`, press Enter
   - Or search "ODBC Data Sources" in Windows Start Menu

2. **Create System DSN**:
   - Go to "System DSN" tab → Click "Add"
   - Select "ODBC Driver 17 for SQL Server" → Click "Finish"

3. **Configure DSN**:
   - Name: `videogames`
   - Description: Video Game Sales Data Warehouse
   - Server: `localhost` (or `localhost\SQLEXPRESS` for named instance)

4. **Authentication**:
   - Choose "With SQL Server authentication"
   - Login ID: `sa` (or your preferred username)
   - Password: [Your SQL Server password]

5. **Database Configuration**:
   - Check "Change the default database to:"
   - Select: `VideoGamesDW`
   - Click "Next" → "Finish"

6. **Test Connection**:
   - Click "Test Data Source"
   - Should see "TESTS COMPLETED SUCCESSFULLY!"

### Power BI Connection

1. **Open Power BI Desktop**
2. **Get Data** → **More...** → **ODBC** → **Connect**
3. **Select Data Source Name**: Choose "videogames" from dropdown
4. **Select Tables**: Choose all dimension and fact tables
5. **Create Relationships**:
   - `game_sales_fact[platform_id]` → `platform_dim[platform_id]`
   - `game_sales_fact[genre_id]` → `genre_dim[genre_id]`
   - `game_sales_fact[publisher_id]` → `publisher_dim[publisher_id]`
   - `game_sales_fact[time_id]` → `time_dim[time_id]`

## 7. Current File Structure

```
bi-video-game-sales-analysis/
├── data/
│   ├── raw/
│   │   └── vgsales.csv                 # Original Kaggle dataset
│   ├── prepared/
│   │   └── vgsales_cleaned.csv         # Cleaned data from data_prep.py ✅
│   └── dw/
│       ├── video_games_dw.sqlite       # SQLite database (backup/legacy)
│       └── video_game_sales_analysis.pbix  # Power BI dashboard 🚧
├── src/
│   └── analytics_project/
│       ├── data_prep.py               # Data preparation script ✅
│       ├── etl_to_dw.py               # SQL Server ETL script ✅
│       └── utils_logger.py            # Logging configuration
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
1. Open `data/dw/video_game_sales_analysis.pbix` in Power BI Desktop
2. **Data Source**: Connected via ODBC System DSN "videogames" to SQL Server
3. **Data Model**: Star schema with proper relationships between fact and dimension tables
4. **OLAP Operations**:
   - **Slicing**: Use year and genre filters
   - **Dicing**: Analyze platform-genre combinations  
   - **Drilldown**: Explore publisher → platform → game hierarchies
   - **Roll-up**: Aggregate regional sales to global totals

## 📊 Dashboard Features

### **Interactive Capabilities:**
- Cross-filtering between all visuals
- Regional segmentation (4 major markets)
- Time-based analysis (1980-2020)
- Platform-genre performance matrix
- Publisher-platform relationships

### **Technical Achievements:**
- Custom DAX measures for coordinate-based mapping
- Conditional formatting in matrix visuals
- Star schema optimization for query performance
- ODBC integration with SQL Server

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
- Ensure SQL Server database is built before opening Power BI file
- Verify System DSN "videogames" is properly configured
- Test connection in ODBC Data Source Administrator first

**Module Import Errors:**
```bash
uv sync --extra dev --extra docs --upgrade
```

**Pre-commit Hook Failures:**
```bash
uv run pre-commit run --all-files
```

### System DSN Issues

**"Data source name not found"**:
- Verify ODBC Data Source Administrator is 64-bit version
- Check DSN name is exactly "videogames"
- Ensure SQL Server is running

**Authentication Failed**:
- Verify SQL Server authentication mode is enabled
- Check username/password in DSN configuration
- Test connection in ODBC administrator first

**Database Not Found**:
- Run etl_to_dw.py to create VideoGamesDW database
- Verify default database is set to VideoGamesDW in DSN

### Data-Specific Issues

**Missing Regional Sales Data**:
- Some older games may have incomplete regional breakdown
- Analysis focuses on relative patterns rather than absolute values

**Platform Name Variations**:
- Dataset uses consistent platform naming conventions
- Legacy platforms grouped appropriately for analysis

### Performance Tips

**Large Dataset Handling**:
- Dataset is optimized for efficient querying
- Power BI aggregations used for improved performance
- Consider data model simplification for very large future expansions

---

## 🔄 Project Completion Status

- [x] Complete data validation and quality checks ✅
- [x] Build data preparation pipeline ✅  
- [x] Implement SQL Server data warehouse ✅
- [x] Set up System DSN ("videogames") ✅
- [x] Create Power BI file with ODBC connection ✅
- [x] Build core visualizations and dashboard layout ✅
- [x] Implement advanced OLAP operations and DAX measures ✅
- [x] Create 3-page interactive dashboard ✅
- [ ] Business insight documentation 🚧
- [ ] Final project presentation 🚧



---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Kaggle for the Video Game Sales dataset
- Power BI community for OLAP operation guidance  
- Graduate program instructors for project framework

---

*Last updated: November 26, 2025*
*Status: PROJECT COMPLETE - 3-Page Interactive Dashboard Delivered*