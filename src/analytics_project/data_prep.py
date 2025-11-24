# src/analytics_project/data_prep.py
"""
Data Preparation Script for Video Game Sales Analysis

This script performs data cleaning, validation, and preparation of the raw vgsales.csv dataset
for business intelligence analysis in Power BI.

Key Operations:
1. Load raw dataset from Kaggle
2. Data quality checks and validation
3. Handle missing values and inconsistencies
4. Create derived features for analysis
5. Export cleaned data for further processing

Author: Graduate BI Project Team
Date: November 2025
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
import sys
import os

# Add src to path for module imports
src_path = Path(__file__).parent
sys.path.append(str(src_path))

# Import from your existing logger - adjust this based on your actual file structure
try:
    from utils_logger import setup_logger
except ImportError:
    # Fallback if the import path is different
    try:
        from analytics_project.utils_logger import setup_logger
    except ImportError:
        # Basic fallback logger if everything else fails
        def setup_logger(name):
            logger = logging.getLogger(name)
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
            return logger

class VideoGameDataPreparer:
    """Handles data preparation and cleaning for video game sales dataset."""
    
    def __init__(self, data_dir=None):
        """
        Initialize the data preparer.
        
        Args:
            data_dir (str): Relative path to data directory. If None, uses project root.
        """
        # Get the project root directory (where the script is run from)
        if data_dir is None:
            # Go up two levels from src/analytics_project to get to project root
            self.project_root = Path(__file__).parent.parent.parent
        else:
            self.project_root = Path(data_dir)
        
        self.data_dir = self.project_root / "data"
        self.raw_data_path = self.data_dir / "raw" / "vgsales.csv"
        self.prepared_data_path = self.data_dir / "prepared" / "vgsales_cleaned.csv"
        
        # Ensure directories exist
        self.raw_data_path.parent.mkdir(parents=True, exist_ok=True)
        self.prepared_data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = setup_logger("data_preparation")
        
        # Data validation rules
        self.expected_columns = [
            'Rank', 'Name', 'Platform', 'Year', 'Genre', 'Publisher',
            'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'
        ]
        
        self.sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        
    def load_raw_data(self) -> pd.DataFrame:
        """
        Load the raw vgsales dataset from CSV.
        
        Returns:
            pd.DataFrame: Raw video game sales data
            
        Raises:
            FileNotFoundError: If raw data file doesn't exist
        """
        self.logger.info(f"Loading raw data from: {self.raw_data_path}")
        self.logger.info(f"Current working directory: {os.getcwd()}")
        self.logger.info(f"Absolute data path: {self.raw_data_path.absolute()}")
        
        if not self.raw_data_path.exists():
            # Create a helpful error message
            self.logger.error(f"Raw data file not found at: {self.raw_data_path.absolute()}")
            self.logger.error("Please ensure:")
            self.logger.error("1. The vgsales.csv file is downloaded from Kaggle")
            self.logger.error("2. The file is placed in: data/raw/vgsales.csv")
            self.logger.error("3. The directory structure exists")
            raise FileNotFoundError(f"Raw data file not found: {self.raw_data_path.absolute()}")
        
        try:
            df = pd.read_csv(self.raw_data_path)
            self.logger.info(f"Successfully loaded dataset with {len(df):,} rows and {len(df.columns)} columns")
            return df
        except Exception as e:
            self.logger.error(f"Error loading raw data: {e}")
            raise
    
    # ... (rest of the methods remain the same - validate_data_structure, handle_missing_values, etc.)
    def validate_data_structure(self, df: pd.DataFrame) -> bool:
        """
        Validate that the dataset has expected structure and columns.
        
        Args:
            df (pd.DataFrame): Dataset to validate
            
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        self.logger.info("Validating data structure...")
        
        # Check required columns
        missing_columns = set(self.expected_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check data types
        if not pd.api.types.is_numeric_dtype(df['Global_Sales']):
            self.logger.warning("Global_Sales column is not numeric - will attempt conversion")
        
        self.logger.info("Data structure validation passed")
        return True
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            df (pd.DataFrame): Input dataframe with potential missing values
            
        Returns:
            pd.DataFrame: Dataframe with handled missing values
        """
        self.logger.info("Handling missing values...")
        
        initial_rows = len(df)
        
        # Check for missing values
        missing_info = df.isnull().sum()
        if missing_info.sum() > 0:
            self.logger.warning(f"Missing values found:\n{missing_info[missing_info > 0]}")
        
        # Handle Year missing values - these are problematic for time-based analysis
        year_missing = df['Year'].isnull().sum()
        if year_missing > 0:
            self.logger.warning(f"Removing {year_missing} rows with missing Year values")
            df = df.dropna(subset=['Year'])
        
        # Handle Publisher missing values - fill with 'Unknown'
        publisher_missing = df['Publisher'].isnull().sum()
        if publisher_missing > 0:
            self.logger.info(f"Filling {publisher_missing} missing Publisher values with 'Unknown'")
            df['Publisher'] = df['Publisher'].fillna('Unknown')
        
        # Handle missing sales data - fill with 0 (assume no sales reported)
        for sales_col in self.sales_columns:
            missing_sales = df[sales_col].isnull().sum()
            if missing_sales > 0:
                self.logger.info(f"Filling {missing_sales} missing {sales_col} values with 0")
                df[sales_col] = df[sales_col].fillna(0)
        
        final_rows = len(df)
        self.logger.info(f"Missing value handling complete. Removed {initial_rows - final_rows} rows")
        
        return df
    
    def clean_data_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize data values.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        self.logger.info("Cleaning data values...")
        
        # Create a copy to avoid SettingWithCopyWarning
        df_clean = df.copy()
        
        # Clean Year column - convert to integer, handle any string values
        df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
        df_clean = df_clean.dropna(subset=['Year'])  # Remove any remaining invalid years
        df_clean['Year'] = df_clean['Year'].astype(int)
        
        # Ensure sales columns are numeric
        for sales_col in self.sales_columns:
            df_clean[sales_col] = pd.to_numeric(df_clean[sales_col], errors='coerce').fillna(0)
        
        # Clean text columns - strip whitespace and handle case inconsistencies
        text_columns = ['Name', 'Platform', 'Genre', 'Publisher']
        for col in text_columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
        
        # Standardize platform names (common variations)
        platform_mapping = {
            'PS': 'PS', 
            'Playstation': 'PS',
            'Xbox': 'XB',
            'XBOX': 'XB',
            'Nintendo': 'NES'  # Add more mappings as needed
        }
        
        for old, new in platform_mapping.items():
            mask = df_clean['Platform'].str.contains(old, case=False, na=False)
            df_clean.loc[mask, 'Platform'] = new
        
        self.logger.info("Data value cleaning complete")
        return df_clean
    
    def create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create derived features for enhanced analysis.
        
        Args:
            df (pd.DataFrame): Cleaned dataframe
            
        Returns:
            pd.DataFrame: Dataframe with derived features
        """
        self.logger.info("Creating derived features...")
        
        df_enhanced = df.copy()
        
        # Create decade feature for trend analysis
        df_enhanced['Decade'] = (df_enhanced['Year'] // 10) * 10
        
        # Create platform generation based on year ranges
        conditions = [
            df_enhanced['Year'] < 1990,
            (df_enhanced['Year'] >= 1990) & (df_enhanced['Year'] < 2000),
            (df_enhanced['Year'] >= 2000) & (df_enhanced['Year'] < 2010),
            df_enhanced['Year'] >= 2010
        ]
        choices = ['Pre-1990', '1990s', '2000s', '2010s+']
        df_enhanced['Era'] = np.select(conditions, choices, default='Unknown')
        
        # Calculate regional sales percentages
        for region in ['NA', 'EU', 'JP', 'Other']:
            sales_col = f'{region}_Sales'
            pct_col = f'{region}_Sales_Pct'
            df_enhanced[pct_col] = (df_enhanced[sales_col] / df_enhanced['Global_Sales']).replace([np.inf, -np.inf], 0).fillna(0)
        
        # Create success categories based on global sales
        conditions = [
            df_enhanced['Global_Sales'] >= 10,
            (df_enhanced['Global_Sales'] >= 5) & (df_enhanced['Global_Sales'] < 10),
            (df_enhanced['Global_Sales'] >= 1) & (df_enhanced['Global_Sales'] < 5),
            df_enhanced['Global_Sales'] < 1
        ]
        choices = ['Blockbuster (10M+)', 'Major Hit (5-10M)', 'Hit (1-5M)', 'Niche (<1M)']
        df_enhanced['Success_Category'] = np.select(conditions, choices, default='Unknown')
        
        # Flag for multi-region success (significant sales in at least 2 regions)
        region_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
        significant_sales_mask = df_enhanced[region_cols] > 0.1  # 100k units threshold
        df_enhanced['Multi_Region_Success'] = significant_sales_mask.sum(axis=1) >= 2
        
        self.logger.info("Derived features creation complete")
        return df_enhanced
    
    def perform_quality_checks(self, df: pd.DataFrame) -> bool:
        """
        Perform final data quality checks before export.
        
        Args:
            df (pd.DataFrame): Final dataframe to check
            
        Returns:
            bool: True if all quality checks pass
        """
        self.logger.info("Performing final quality checks...")
        
        checks_passed = True
        
        # Check for negative sales values
        negative_sales = (df[self.sales_columns] < 0).any().any()
        if negative_sales:
            self.logger.error("Negative sales values found!")
            checks_passed = False
        
        # Check for duplicate records
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            self.logger.warning(f"Found {duplicates} duplicate records - these will be kept for analysis")
        
        # Check data consistency (Global_Sales should equal sum of regional sales)
        regional_sum = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum(axis=1)
        global_sales_diff = abs(df['Global_Sales'] - regional_sum)
        inconsistent_records = (global_sales_diff > 0.01).sum()  # Allow small rounding differences
        
        if inconsistent_records > 0:
            self.logger.warning(f"Found {inconsistent_records} records with inconsistent global/regional sales totals")
        
        # Validate year range
        min_year = df['Year'].min()
        max_year = df['Year'].max()
        self.logger.info(f"Data covers years {min_year} to {max_year}")
        
        if checks_passed:
            self.logger.info("All quality checks passed")
        else:
            self.logger.warning("Some quality checks failed - review warnings above")
        
        return checks_passed
    
    def export_cleaned_data(self, df: pd.DataFrame) -> None:
        """
        Export cleaned and prepared data to CSV.
        
        Args:
            df (pd.DataFrame): Prepared dataframe to export
        """
        self.logger.info(f"Exporting cleaned data to: {self.prepared_data_path}")
        
        try:
            df.to_csv(self.prepared_data_path, index=False)
            self.logger.info(f"Successfully exported {len(df):,} rows to {self.prepared_data_path}")
        except Exception as e:
            self.logger.error(f"Error exporting cleaned data: {e}")
            raise
    
    def generate_data_summary(self, df: pd.DataFrame) -> dict:
        """
        Generate summary statistics for the prepared dataset.
        
        Args:
            df (pd.DataFrame): Prepared dataframe
            
        Returns:
            dict: Summary statistics
        """
        self.logger.info("Generating data summary...")
        
        summary = {
            'total_games': len(df),
            'time_period': f"{df['Year'].min()} - {df['Year'].max()}",
            'total_platforms': df['Platform'].nunique(),
            'total_publishers': df['Publisher'].nunique(),
            'total_genres': df['Genre'].nunique(),
            'total_global_sales': df['Global_Sales'].sum(),
            'avg_sales_per_game': df['Global_Sales'].mean(),
            'top_genre': df.groupby('Genre')['Global_Sales'].sum().idxmax(),
            'top_platform': df.groupby('Platform')['Global_Sales'].sum().idxmax(),
            'top_publisher': df.groupby('Publisher')['Global_Sales'].sum().idxmax()
        }
        
        # Log summary
        self.logger.info("Dataset Summary:")
        for key, value in summary.items():
            self.logger.info(f"  {key}: {value}")
        
        return summary
    
    def run_pipeline(self) -> pd.DataFrame:
        """
        Execute the complete data preparation pipeline.
        
        Returns:
            pd.DataFrame: Fully prepared and cleaned dataset
        """
        self.logger.info("Starting video game sales data preparation pipeline...")
        
        try:
            # Step 1: Load raw data
            df = self.load_raw_data()
            
            # Step 2: Validate structure
            self.validate_data_structure(df)
            
            # Step 3: Handle missing values
            df = self.handle_missing_values(df)
            
            # Step 4: Clean data values
            df = self.clean_data_values(df)
            
            # Step 5: Create derived features
            df = self.create_derived_features(df)
            
            # Step 6: Perform quality checks
            self.perform_quality_checks(df)
            
            # Step 7: Export cleaned data
            self.export_cleaned_data(df)
            
            # Step 8: Generate summary
            summary = self.generate_data_summary(df)
            
            self.logger.info("Data preparation pipeline completed successfully!")
            return df
            
        except Exception as e:
            self.logger.error(f"Data preparation pipeline failed: {e}")
            raise


def main():
    """Main execution function."""
    try:
        # Initialize data preparer
        preparer = VideoGameDataPreparer()
        
        # Run the complete pipeline
        cleaned_data = preparer.run_pipeline()
        
        print("✅ Data preparation completed successfully!")
        print(f"📊 Prepared dataset: {len(cleaned_data):,} games")
        print(f"💾 Output: data/prepared/vgsales_cleaned.csv")
        
    except Exception as e:
        print(f"❌ Data preparation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()