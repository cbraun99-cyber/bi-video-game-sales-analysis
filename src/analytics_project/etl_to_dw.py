# src/analytics_project/etl_to_dw.py
"""
ETL to Data Warehouse Script for Video Game Sales Analysis

This script loads the cleaned video game sales data into a SQLite data warehouse
with a star schema optimized for OLAP operations in Power BI.

Star Schema Design:
- Fact Table: game_sales_fact
- Dimension Tables: game_dim, platform_dim, genre_dim, publisher_dim, time_dim

Author: Graduate BI Project Team
Date: November 2025
"""

import pandas as pd
import sqlite3
import logging
from pathlib import Path
import sys
from datetime import datetime

# Add src to path for module imports
src_path = Path(__file__).parent
sys.path.append(str(src_path))

# Import from your existing logger
try:
    from utils_logger import setup_logger
except ImportError:
    # Basic fallback logger
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


class VideoGameDataWarehouse:
    """Handles ETL process to load video game data into SQLite data warehouse."""
    
    def __init__(self, data_dir=None):
        """
        Initialize the data warehouse ETL processor.
        
        Args:
            data_dir (str): Relative path to data directory. If None, uses project root.
        """
        # Get the project root directory
        if data_dir is None:
            self.project_root = Path(__file__).parent.parent.parent
        else:
            self.project_root = Path(data_dir)
        
        self.data_dir = self.project_root / "data"
        self.dw_dir = self.data_dir / "dw"
        self.cleaned_data_path = self.data_dir / "prepared" / "vgsales_cleaned.csv"
        self.dw_path = self.dw_dir / "video_games_dw.sqlite"
        
        # Ensure directories exist
        self.dw_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = setup_logger("etl_to_dw")
        
    def create_connection(self) -> sqlite3.Connection:
        """
        Create and return SQLite database connection.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        self.logger.info(f"Creating database connection: {self.dw_path}")
        try:
            conn = sqlite3.connect(self.dw_path)
            conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
            return conn
        except Exception as e:
            self.logger.error(f"Error creating database connection: {e}")
            raise
    
    def create_dimension_tables(self, conn: sqlite3.Connection) -> None:
        """
        Create dimension tables for the star schema.
        
        Args:
            conn (sqlite3.Connection): Database connection
        """
        self.logger.info("Creating dimension tables...")
        
        # Platform Dimension
        conn.execute("""
        CREATE TABLE IF NOT EXISTS platform_dim (
            platform_id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform_name TEXT UNIQUE NOT NULL,
            platform_category TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Genre Dimension
        conn.execute("""
        CREATE TABLE IF NOT EXISTS genre_dim (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_name TEXT UNIQUE NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Publisher Dimension
        conn.execute("""
        CREATE TABLE IF NOT EXISTS publisher_dim (
            publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            publisher_name TEXT UNIQUE NOT NULL,
            publisher_size_category TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Time Dimension
        conn.execute("""
        CREATE TABLE IF NOT EXISTS time_dim (
            time_id INTEGER PRIMARY KEY,
            year INTEGER NOT NULL,
            decade INTEGER NOT NULL,
            era TEXT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Game Dimension (Degenerate dimension from fact table)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS game_dim (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL,
            platform_id INTEGER,
            genre_id INTEGER,
            publisher_id INTEGER,
            release_year INTEGER,
            success_category TEXT,
            multi_region_success BOOLEAN,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (platform_id) REFERENCES platform_dim (platform_id),
            FOREIGN KEY (genre_id) REFERENCES genre_dim (genre_id),
            FOREIGN KEY (publisher_id) REFERENCES publisher_dim (publisher_id)
        )
        """)
        
        self.logger.info("Dimension tables created successfully")
    
    def create_fact_table(self, conn: sqlite3.Connection) -> None:
        """
        Create the fact table for sales metrics.
        
        Args:
            conn (sqlite3.Connection): Database connection
        """
        self.logger.info("Creating fact table...")
        
        conn.execute("""
        CREATE TABLE IF NOT EXISTS game_sales_fact (
            fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            platform_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            publisher_id INTEGER NOT NULL,
            time_id INTEGER NOT NULL,
            
            -- Sales Metrics (Measures)
            global_sales REAL NOT NULL,
            na_sales REAL NOT NULL,
            eu_sales REAL NOT NULL,
            jp_sales REAL NOT NULL,
            other_sales REAL NOT NULL,
            
            -- Derived Metrics
            na_sales_pct REAL,
            eu_sales_pct REAL,
            jp_sales_pct REAL,
            other_sales_pct REAL,
            
            -- Metadata
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Foreign Key Constraints
            FOREIGN KEY (game_id) REFERENCES game_dim (game_id),
            FOREIGN KEY (platform_id) REFERENCES platform_dim (platform_id),
            FOREIGN KEY (genre_id) REFERENCES genre_dim (genre_id),
            FOREIGN KEY (publisher_id) REFERENCES publisher_dim (publisher_id),
            FOREIGN KEY (time_id) REFERENCES time_dim (time_id),
            
            -- Composite unique constraint
            UNIQUE (game_id, platform_id, genre_id, publisher_id, time_id)
        )
        """)
        
        self.logger.info("Fact table created successfully")
    
    def load_dimension_data(self, conn: sqlite3.Connection, df: pd.DataFrame) -> dict:
        """
        Load data into dimension tables and return mapping dictionaries.
        
        Args:
            conn (sqlite3.Connection): Database connection
            df (pd.DataFrame): Cleaned source data
            
        Returns:
            dict: Dictionary with dimension ID mappings
        """
        self.logger.info("Loading dimension data...")
        
        dimension_mappings = {}
        
        # Load Platform Dimension
        platforms = df['Platform'].unique()
        platform_map = {}
        for platform in platforms:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO platform_dim (platform_name) VALUES (?)",
                (platform,)
            )
            # Get the platform_id
            if cursor.lastrowid:
                platform_map[platform] = cursor.lastrowid
            else:
                # If row already exists, get existing ID
                result = conn.execute(
                    "SELECT platform_id FROM platform_dim WHERE platform_name = ?",
                    (platform,)
                ).fetchone()
                platform_map[platform] = result[0] if result else None
        
        dimension_mappings['platform'] = platform_map
        self.logger.info(f"Loaded {len(platform_map)} platforms")
        
        # Load Genre Dimension
        genres = df['Genre'].unique()
        genre_map = {}
        for genre in genres:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO genre_dim (genre_name) VALUES (?)",
                (genre,)
            )
            if cursor.lastrowid:
                genre_map[genre] = cursor.lastrowid
            else:
                result = conn.execute(
                    "SELECT genre_id FROM genre_dim WHERE genre_name = ?",
                    (genre,)
                ).fetchone()
                genre_map[genre] = result[0] if result else None
        
        dimension_mappings['genre'] = genre_map
        self.logger.info(f"Loaded {len(genre_map)} genres")
        
        # Load Publisher Dimension
        publishers = df['Publisher'].unique()
        publisher_map = {}
        for publisher in publishers:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO publisher_dim (publisher_name) VALUES (?)",
                (publisher,)
            )
            if cursor.lastrowid:
                publisher_map[publisher] = cursor.lastrowid
            else:
                result = conn.execute(
                    "SELECT publisher_id FROM publisher_dim WHERE publisher_name = ?",
                    (publisher,)
                ).fetchone()
                publisher_map[publisher] = result[0] if result else None
        
        dimension_mappings['publisher'] = publisher_map
        self.logger.info(f"Loaded {len(publisher_map)} publishers")
        
        # Load Time Dimension
        time_map = {}
        years = df['Year'].unique()
        for year in years:
            decade = (year // 10) * 10
            era = self._get_era(year)
            time_id = int(f"{year}")  # Simple time_id based on year
            
            cursor = conn.execute("""
                INSERT OR IGNORE INTO time_dim (time_id, year, decade, era) 
                VALUES (?, ?, ?, ?)
            """, (time_id, year, decade, era))
            
            time_map[year] = time_id
        
        dimension_mappings['time'] = time_map
        self.logger.info(f"Loaded {len(time_map)} time periods")
        
        return dimension_mappings
    
    def _get_era(self, year: int) -> str:
        """Helper method to determine era based on year."""
        if year < 1990:
            return 'Pre-1990'
        elif 1990 <= year < 2000:
            return '1990s'
        elif 2000 <= year < 2010:
            return '2000s'
        else:
            return '2010s+'
    
    def load_game_dimension(self, conn: sqlite3.Connection, df: pd.DataFrame, dim_mappings: dict) -> dict:
        """
        Load game dimension data and return game ID mappings.
        
        Args:
            conn (sqlite3.Connection): Database connection
            df (pd.DataFrame): Cleaned source data
            dim_mappings (dict): Dimension ID mappings
            
        Returns:
            dict: Game ID mappings
        """
        self.logger.info("Loading game dimension data...")
        
        game_map = {}
        
        # Create a unique identifier for each game
        for _, row in df.iterrows():
            game_name = row['Name']
            platform_id = dim_mappings['platform'].get(row['Platform'])
            genre_id = dim_mappings['genre'].get(row['Genre'])
            publisher_id = dim_mappings['publisher'].get(row['Publisher'])
            
            # Create composite key for game uniqueness
            composite_key = f"{game_name}_{platform_id}_{genre_id}_{publisher_id}"
            
            if composite_key not in game_map:
                cursor = conn.execute("""
                    INSERT INTO game_dim (
                        game_name, platform_id, genre_id, publisher_id, 
                        release_year, success_category, multi_region_success
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    game_name, platform_id, genre_id, publisher_id,
                    row['Year'], row.get('Success_Category', 'Unknown'),
                    row.get('Multi_Region_Success', False)
                ))
                
                game_map[composite_key] = cursor.lastrowid
        
        self.logger.info(f"Loaded {len(game_map)} unique games")
        return game_map
    
    def load_fact_data(self, conn: sqlite3.Connection, df: pd.DataFrame, dim_mappings: dict, game_map: dict) -> None:
        """
        Load sales data into fact table.
        
        Args:
            conn (sqlite3.Connection): Database connection
            df (pd.DataFrame): Cleaned source data
            dim_mappings (dict): Dimension ID mappings
            game_map (dict): Game ID mappings
        """
        self.logger.info("Loading fact data...")
        
        fact_count = 0
        batch_size = 1000
        batch_data = []
        
        for _, row in df.iterrows():
            # Get dimension IDs
            platform_id = dim_mappings['platform'].get(row['Platform'])
            genre_id = dim_mappings['genre'].get(row['Genre'])
            publisher_id = dim_mappings['publisher'].get(row['Publisher'])
            time_id = dim_mappings['time'].get(row['Year'])
            
            # Get game_id using composite key
            composite_key = f"{row['Name']}_{platform_id}_{genre_id}_{publisher_id}"
            game_id = game_map.get(composite_key)
            
            if all([game_id, platform_id, genre_id, publisher_id, time_id]):
                batch_data.append((
                    game_id, platform_id, genre_id, publisher_id, time_id,
                    row['Global_Sales'], row['NA_Sales'], row['EU_Sales'], 
                    row['JP_Sales'], row['Other_Sales'],
                    row.get('NA_Sales_Pct', 0), row.get('EU_Sales_Pct', 0),
                    row.get('JP_Sales_Pct', 0), row.get('Other_Sales_Pct', 0)
                ))
                
                fact_count += 1
                
                # Insert in batches for performance
                if len(batch_data) >= batch_size:
                    conn.executemany("""
                        INSERT OR IGNORE INTO game_sales_fact (
                            game_id, platform_id, genre_id, publisher_id, time_id,
                            global_sales, na_sales, eu_sales, jp_sales, other_sales,
                            na_sales_pct, eu_sales_pct, jp_sales_pct, other_sales_pct
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, batch_data)
                    batch_data = []
        
        # Insert remaining records
        if batch_data:
            conn.executemany("""
                INSERT OR IGNORE INTO game_sales_fact (
                    game_id, platform_id, genre_id, publisher_id, time_id,
                    global_sales, na_sales, eu_sales, jp_sales, other_sales,
                    na_sales_pct, eu_sales_pct, jp_sales_pct, other_sales_pct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch_data)
        
        self.logger.info(f"Loaded {fact_count} fact records")
    
    def create_indexes(self, conn: sqlite3.Connection) -> None:
        """
        Create indexes for optimal query performance.
        
        Args:
            conn (sqlite3.Connection): Database connection
        """
        self.logger.info("Creating indexes...")
        
        # Fact table indexes
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_fact_game ON game_sales_fact(game_id)",
            "CREATE INDEX IF NOT EXISTS idx_fact_platform ON game_sales_fact(platform_id)",
            "CREATE INDEX IF NOT EXISTS idx_fact_genre ON game_sales_fact(genre_id)",
            "CREATE INDEX IF NOT EXISTS idx_fact_publisher ON game_sales_fact(publisher_id)",
            "CREATE INDEX IF NOT EXISTS idx_fact_time ON game_sales_fact(time_id)",
            "CREATE INDEX IF NOT EXISTS idx_fact_global_sales ON game_sales_fact(global_sales)",
            
            # Dimension table indexes
            "CREATE INDEX IF NOT EXISTS idx_platform_name ON platform_dim(platform_name)",
            "CREATE INDEX IF NOT EXISTS idx_genre_name ON genre_dim(genre_name)",
            "CREATE INDEX IF NOT EXISTS idx_publisher_name ON publisher_dim(publisher_name)",
            "CREATE INDEX IF NOT EXISTS idx_time_year ON time_dim(year)",
            "CREATE INDEX IF NOT EXISTS idx_game_name ON game_dim(game_name)",
        ]
        
        for index_sql in indexes:
            conn.execute(index_sql)
        
        self.logger.info("Indexes created successfully")
    
    def validate_data_warehouse(self, conn: sqlite3.Connection) -> bool:
        """
        Validate the data warehouse integrity and content.
        
        Args:
            conn (sqlite3.Connection): Database connection
            
        Returns:
            bool: True if validation passes
        """
        self.logger.info("Validating data warehouse...")
        
        validation_queries = {
            "Total Games": "SELECT COUNT(*) FROM game_dim",
            "Total Fact Records": "SELECT COUNT(*) FROM game_sales_fact",
            "Total Platforms": "SELECT COUNT(*) FROM platform_dim",
            "Total Genres": "SELECT COUNT(*) FROM genre_dim",
            "Total Publishers": "SELECT COUNT(*) FROM publisher_dim",
            "Total Time Periods": "SELECT COUNT(*) FROM time_dim",
            "Total Global Sales": "SELECT SUM(global_sales) FROM game_sales_fact",
        }
        
        self.logger.info("Data Warehouse Summary:")
        for metric, query in validation_queries.items():
            result = conn.execute(query).fetchone()[0]
            self.logger.info(f"  {metric}: {result:,}")
        
        # Check for orphaned records
        orphan_check = """
        SELECT COUNT(*) FROM game_sales_fact fact
        LEFT JOIN game_dim g ON fact.game_id = g.game_id
        WHERE g.game_id IS NULL
        """
        orphan_count = conn.execute(orphan_check).fetchone()[0]
        
        if orphan_count > 0:
            self.logger.warning(f"Found {orphan_count} orphaned fact records")
            return False
        
        self.logger.info("Data warehouse validation passed")
        return True
    
    def run_etl_pipeline(self) -> None:
        """
        Execute the complete ETL pipeline.
        """
        self.logger.info("Starting ETL pipeline to data warehouse...")
        
        # Check if cleaned data exists
        if not self.cleaned_data_path.exists():
            self.logger.error(f"Cleaned data file not found: {self.cleaned_data_path}")
            self.logger.error("Please run data_preparation.py first")
            raise FileNotFoundError(f"Cleaned data file not found: {self.cleaned_data_path}")
        
        conn = None
        try:
            # Load cleaned data
            self.logger.info(f"Loading cleaned data from: {self.cleaned_data_path}")
            df = pd.read_csv(self.cleaned_data_path)
            self.logger.info(f"Loaded {len(df):,} records for ETL processing")
            
            # Create database connection
            conn = self.create_connection()
            
            # Step 1: Create dimension tables
            self.create_dimension_tables(conn)
            
            # Step 2: Create fact table
            self.create_fact_table(conn)
            
            # Step 3: Load dimension data
            dim_mappings = self.load_dimension_data(conn, df)
            
            # Step 4: Load game dimension
            game_map = self.load_game_dimension(conn, df, dim_mappings)
            
            # Step 5: Load fact data
            self.load_fact_data(conn, df, dim_mappings, game_map)
            
            # Step 6: Create indexes
            self.create_indexes(conn)
            
            # Step 7: Validate
            self.validate_data_warehouse(conn)
            
            # Commit all changes
            conn.commit()
            
            self.logger.info("ETL pipeline completed successfully!")
            
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"ETL pipeline failed: {e}")
            raise
        finally:
            if conn:
                conn.close()


def main():
    """Main execution function."""
    try:
        # Initialize ETL processor
        etl_processor = VideoGameDataWarehouse()
        
        # Run the complete ETL pipeline
        etl_processor.run_etl_pipeline()
        
        print("✅ ETL to Data Warehouse completed successfully!")
        print(f"💾 Data warehouse: data/dw/video_games_dw.sqlite")
        print("📊 Star schema ready for Power BI analysis!")
        
    except Exception as e:
        print(f"❌ ETL to Data Warehouse failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()