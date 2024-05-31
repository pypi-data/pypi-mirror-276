## File for S3 I/O operations (uploading, downloading, etc.)

import boto3
from mb_pandas.src.dfload import load_any_df
from io import BytesIO
from PIL import Image
import numpy as np
from mb_pandas.src import remove_unnamed

__all__ = ["upload_df", "download_df", "upload_image", "download_image","get_response","get_image"]

def get_client():
    """
    Returns a boto3 client for S3
    """
    return boto3.client('s3')

def get_response(client, bucket, key):
    """
    Returns the response object for a given bucket and key
    """
    return client.get_object(Bucket=bucket, Key=key)

def get_image(response):
    """
    Returns an image object from the response object
    """
    return Image.open(BytesIO(response['Body'].read()))

def upload_df(df, bucket, key, client=None):
    """
    Uploads a dataframe to S3
    """
    if client is None:
        client = get_client()
    df = remove_unnamed(df)
    client.put_object(Bucket=bucket, Key=key, Body=df)

def download_df(bucket, key, client=None):
    """ 
    Downloads a dataframe from S3
    """
    if client is None:
        client = get_client()
    response = get_response(client, bucket, key)
    return load_any_df(BytesIO(response['Body'].read()))

def upload_image(image, bucket, key, client=None):
    """
    Uploads an image to S3
    """
    if client is None:
        client = get_client()
    client.put_object(Bucket=bucket, Key=key, Body=image)

def download_image(bucket, key, client=None):
    """
    Downloads an image from S3
    """
    if client is None:
        client = get_client()
    response = get_response(client, bucket, key)
    return get_image(response)
    
