import awswrangler as wr
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load your AWS keys from the .env file
load_dotenv()


DB_ENDPOINT = "euro-coffee-db.cix2wuay6je4.us-east-1.rds.amazonaws.com"
DB_PASSWORD = "admin1234"
S3_CLEAN_PATH = "s3://euro-coffee-cleaned/top_eu_roasters/"
# ------------------------------------

# Connect to the default 'postgres' database created by RDS
db_url = f"postgresql://postgres:{DB_PASSWORD}@{DB_ENDPOINT}:5432/postgres"
engine = create_engine(db_url)

try:
    print("Fetching clean Parquet data from S3...")
    # awswrangler automatically uses your AWS keys from the .env file!
    clean_df = wr.s3.read_parquet(S3_CLEAN_PATH)

    print("Pouring data into the RDS PostgreSQL database...")
    # This automatically creates a table named 'eu_coffee_metrics' and loads the data
    clean_df.to_sql('eu_coffee_metrics', engine, index=False, if_exists='replace')

    print("Success! The pipeline is complete and the beans are ready for Tableau! ☕📊")

except Exception as e:
    print(f"An error occurred: {e}")