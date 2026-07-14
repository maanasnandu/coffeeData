import os
import boto3

from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv


load_dotenv()

def upload_to_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    try:
        print(f"initiating upload of {local_file} to s3://{bucket}/{s3_file}")
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Uploaded to s3://{bucket}/{s3_file}")

    except ClientError as e:
        print(f"An AWS error occurred: {e}")
    except NoCredentialsError as e:
        print(f"No credentials were found for {local_file}.")
    except FileNotFoundError as e:
        print(f"File not found for {local_file}.")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOCAL_FILE_PATH = os.path.join(BASE_DIR, 'data', 'global_top_100_coffee_shops.csv')

    BUCKET_NAME = 'euro-coffee-raw'
    S3_FILE_NAME = 'global_top_100_coffee_shops.csv'

    upload_to_s3(LOCAL_FILE_PATH, BUCKET_NAME, S3_FILE_NAME)
