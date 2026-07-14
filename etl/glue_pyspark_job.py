import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# 1. Extract - read raw coffee shop data from S3 bucket
input_path = "s3://euro-coffee-raw/global_top_100_coffee_shops.csv"
raw_df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)

# 2. Drop missing data (Updated to use columns that actually exist)
clean_df = raw_df.dropna(subset=["shop_name", "country"])

# 3. Create SQL temp view
clean_df.createOrReplaceTempView("top_100_shops")

# 4. Transformation (Selecting only the exact columns in your CSV)
transformed_df = spark.sql("""
    SELECT 
        rank,
        shop_name,
        country,
        list_name,
        list_year,
        source_url
    FROM top_100_shops
    WHERE shop_name IS NOT NULL
""")

# 5. Load - write clean Parquet data to the target bucket
output_path  = 's3://euro-coffee-cleaned/top_global_shops/'
transformed_df.write.mode('overwrite').parquet(output_path)

print('Transformation complete, clean data has been written to the target bucket. Happy Caffeinating!')