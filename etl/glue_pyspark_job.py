import  sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)


#Extract - read raw coffee data from s3 buck
input_path = "s3://euro-coffee-raw/coffee_analysis.csv"
raw_df = spark.read.option("header", "true").option("inferSchema" , "true").csv(input_path)

#Drop missing data
clean_df = raw_df.dropna(subset=["rating", "roaster", "loc_country"])


#create SQL temp view
clean_df.printSchema()
clean_df.createOrReplaceTempView("coffee_data")

# Transformation
transformed_df = spark.sql(""                   
                           "WITH RankedRoasters AS (SELECT roaster, loc_country, origin_1 as bean_origin, CAST(rating AS FLOAT) AS rating, DENSE_RANK() OVER (PARTITION BY loc_country ORDER BY CAST(rating AS FLOAT) DESC) as country_rank FROM coffee_data WHERE loc_country IN ('France', 'Germany', 'Italy', 'Spain', 'United Kingdom')) SELECT * FROM RankedRoasters WHERE country_rank <= 5" 
                           "")

output_path  = 's3://euro-coffee-cleaned/top_eu_roasters/'
transformed_df.write.mode('overwrite').parquet(output_path)

print('Transformation complete, clean data has been written to the target bucket. Happy Roasting!')