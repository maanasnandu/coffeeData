import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load your AWS keys
load_dotenv()


DB_ENDPOINT = "euro-coffee-db.cix2wuay6je4.us-east-1.rds.amazonaws.com"
DB_PASSWORD = "admin1234"
# ------------------------------------

# Connect to the RDS database
db_url = f"postgresql://postgres:{DB_PASSWORD}@{DB_ENDPOINT}:5432/postgres"
engine = create_engine(db_url)

try:
    print("Connecting to RDS and extracting your clean beans...")

    # Query the exact table we created in the last step
    df = pd.read_sql("SELECT * FROM eu_coffee_metrics", engine)

    # Dynamically find the data folder so it saves in the right spot
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(BASE_DIR, 'data', 'tableau_ready_coffee.csv')

    # Export to a local CSV file
    df.to_csv(output_path, index=False)

    print(f"Success! Data saved to {output_path}")

except Exception as e:
    print(f"An error occurred: {e}")