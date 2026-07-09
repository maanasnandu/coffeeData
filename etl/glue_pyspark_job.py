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
transformed_df = spark.sql("""SELECT
        name AS coffee_name,
        roaster,
        loc_country AS roaster_country,
        roast AS roast_level,
        origin_1 AS bean_origin,
        100g_USD AS price_per_100g,
        rating,
        -- Fun Metric 1: Value for Money (Price per rating point)
        ROUND((100g_USD / rating), 2) AS price_per_point,
        -- Fun Metric 2: Categorizing the coffee tier
        CASE 
            WHEN rating >= 95 THEN 'Exceptional'
            WHEN rating >= 90 THEN 'Outstanding'
            ELSE 'Excellent' 
        END AS quality_tier,
        desc_1 AS primary_flavor,
        desc_2 AS secondary_flavor,
        -- Fun Metric 3: Keeping the country ranking
        DENSE_RANK() OVER (PARTITION BY loc_country ORDER BY rating DESC) as country_rank
    FROM coffee_data
    WHERE 100g_USD IS NOT NULL""")

output_path  = 's3://euro-coffee-cleaned/top_eu_roasters/'
transformed_df.write.mode('overwrite').parquet(output_path)

print('Transformation complete, clean data has been written to the target bucket. Happy Roasting!')