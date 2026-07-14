import awswrangler as wr
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load your AWS keys and DB credentials from the .env file
load_dotenv()

# Pulling credentials securely!
DB_ENDPOINT = os.getenv("DB_ENDPOINT")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# FIXED: Pointing to the new global shops directory
S3_CLEAN_PATH = "s3://euro-coffee-cleaned/top_global_shops/"
# ------------------------------------

# Connect to the default 'postgres' database created by RDS
db_url = f"postgresql://postgres:{DB_PASSWORD}@{DB_ENDPOINT}:5432/postgres"
engine = create_engine(db_url)

try:
    print("Fetching clean Parquet data from S3...")
    clean_df = wr.s3.read_parquet(S3_CLEAN_PATH)

    print("Pouring data into the RDS PostgreSQL database...")
    # This automatically creates a table named 'global_top_100_shops' and loads the data
    clean_df.to_sql('global_top_100_shops', engine, index=False, if_exists='replace')

    print("Success! The pipeline is complete and the shops are ready for mapping! ☕🗺️")

except Exception as e:
    print(f"An error occurred: {e}")