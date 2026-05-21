#!/usr/bin/env python3
"""Direct R2 connection test using the exact credentials from .env"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

import boto3
from botocore.exceptions import ClientError

account_id = os.getenv("R2_ACCOUNT_ID")
access_key = os.getenv("R2_ACCESS_KEY_ID")
secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
bucket = os.getenv("R2_BUCKET_NAME")
endpoint = os.getenv("R2_ENDPOINT_URL")

print(f"Account ID : {account_id}")
print(f"Access Key : {access_key}")
print(f"Bucket     : {bucket}")
print(f"Endpoint   : {endpoint}")
print()

s3 = boto3.client(
    service_name='s3',
    endpoint_url=endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name='auto',
)

# Test 1: List buckets
print("Test 1: List buckets...")
try:
    resp = s3.list_buckets()
    buckets = [b['Name'] for b in resp.get('Buckets', [])]
    print(f"  ✅ Buckets found: {buckets}")
except ClientError as e:
    print(f"  ❌ list_buckets failed: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
except Exception as e:
    print(f"  ❌ list_buckets error: {e}")

# Test 2: Head bucket
print(f"Test 2: HeadBucket on '{bucket}'...")
try:
    s3.head_bucket(Bucket=bucket)
    print(f"  ✅ Bucket '{bucket}' exists and is accessible")
except ClientError as e:
    code = e.response['Error']['Code']
    msg = e.response['Error']['Message']
    print(f"  ❌ head_bucket failed: {code} - {msg}")

# Test 3: Upload a small test object
print("Test 3: Upload test object...")
try:
    s3.put_object(
        Bucket=bucket,
        Key='test/connection_test.txt',
        Body=b'R2 connection test from IT Asset Management System',
        ContentType='text/plain'
    )
    print("  ✅ Upload successful!")
except ClientError as e:
    code = e.response['Error']['Code']
    msg = e.response['Error']['Message']
    print(f"  ❌ put_object failed: {code} - {msg}")
except Exception as e:
    print(f"  ❌ put_object error: {e}")

# Test 4: List objects
print("Test 4: List objects...")
try:
    resp = s3.list_objects_v2(Bucket=bucket, MaxKeys=5)
    objects = [o['Key'] for o in resp.get('Contents', [])]
    print(f"  ✅ Objects: {objects if objects else '(empty bucket)'}")
except ClientError as e:
    code = e.response['Error']['Code']
    msg = e.response['Error']['Message']
    print(f"  ❌ list_objects failed: {code} - {msg}")
except Exception as e:
    print(f"  ❌ list_objects error: {e}")
