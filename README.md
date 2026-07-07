# Euro Coffee Scene (From Bean To Bytes)
Bonjour! Welcome to my Data Engineering portfolio project! This repository houses a cloud-native ETL (Extract, Transform, Load) pipeline built to process, clean, and analyze specialty coffee quality data.

As I prepare to head to France for my Master's in Data Analytics & AI at IÉSEG in Lille, with a great passion for coffee, I decided to build a pipeline to map out the European specialty coffee scene. Whether it's comparing the flavor profiles of an Ethiopian light roast against a Colombian medium roast, or isolating the top-rated roasters in the EU, this architecture turns messy raw CSVs into query-ready insights.

🏗️ Architecture & Tech Stack
IDE Environment: Pycharm

🚀 The Pipeline Lifecycle
1. Extract (The Loading Dock): ✅
A custom Python ingestion script utilizing the boto3 library securely authenticates and uploads local, raw CSV data (Kaggle Coffee Reviews) directly into an euro-coffee-raw Amazon S3 bucket.

2. Transform (The Roaster): 🚧 In Progress
An AWS Glue job spins up a distributed PySpark environment to:

Filter and drop corrupted rows/missing values.

Explode comma-separated flavor note strings into individual rows for categorical analysis.

Utilize Spark SQL to aggregate average cupping scores by country and roaster.

3. Load (The Cafe Display) 🔜 Upcoming:
The finalized, cleaned DataFrames are pushed into an Amazon RDS (PostgreSQL) relational database, structured and optimized to power downstream Business Intelligence dashboards.

        
👨‍💻 About me:
I'm Maanas Muddam, a data professional with over 3 years of experience building robust front-end applications and scalable data pipelines. When I'm not writing PySpark transformations or optimizing SQL queries, you can usually find me hunting down a great pour-over, waking up early for Formula 1 races, watching movies or hiking out shooting wildlife and astrophotography. Cheers!
