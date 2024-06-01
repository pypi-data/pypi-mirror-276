# order_key = upload_document(order_path)
# result = get_extraction_result(order_key)
# output = load_result_from_s3(result)

import logging
import boto3
import json
import pathlib
import hashlib
from botocore.exceptions import ClientError
import urllib.parse
import requests



def _get_hash_from_bytes(content: bytes):
    hash_object = hashlib.sha256()
    hash_object.update(content)
    hash_id = hash_object.hexdigest()
    return hash_id

def _upload_document(content: bytes, s3_bucket: str):
    hash_id = _get_hash_from_bytes(content)
    s3 = boto3.client('s3')
    key = f"input-order-documents/{hash_id}"
    # check if file exists
    try:
        _ = s3.head_object(Bucket=s3_bucket, Key=key)
        logging.info("Content already exists:\n'%s/%s'\n(filename is hash of file content)", s3_bucket, key) 

    except ClientError:
        logging.info("File does not exist in bucket, uploading file")
        s3.put_object(Bucket=s3_bucket, Key=key, Body=content)

    
    return key


def _get_extraction_result(key: str, lambda_function_name: str):
    lambda_client = boto3.client('lambda')
    payload = json.dumps({
        "source_key": key
    })
    
    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='RequestResponse',
        Payload=payload
    )
    response_payload = response['Payload'].read()
    response_payload = json.loads(response_payload)
    return response_payload


def _load_result_from_s3(result_obj, s3_bucket, parts=("positions", "header"), formats=("html", "json")):
    if not (result_obj["body"] == "Success" and result_obj["statusCode"] == 200):
        raise ValueError(f"Error in lambda function: {result_obj}")
    s3 = boto3.client('s3')
    output = dict()
    for part in parts:
        for format_value in formats:
            object_key = f"{part}_{format_value}"
            logging.info("Loading %s from s3", object_key)
            if not object_key in result_obj:
                continue
            uri = result_obj[object_key]
            key = uri.split('mi-order-extraction-service/')[-1]
            obj = s3.get_object(Bucket=s3_bucket, Key=key)
            output[object_key] = obj['Body'].read().decode('utf-8')
    logging.info("result successfully loaded from s3")
    return output

class GetContentException(Exception):
    
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

def _get_content(order_path: str | pathlib.Path):
     # check if order_path is url 
    is_url = False
    if isinstance(order_path, str):
        try:
            result = urllib.parse.urlparse(order_path)
            if all([result.scheme, result.netloc, result.path]):
                logging.info("URL found: %s", order_path)
                is_url = True

        except ValueError:
            logging.info("Path found: %s", order_path)
            is_url = False
        
    if is_url:
        # download the file from the url 
        response = requests.get(order_path)
        # check if the request was successful
        if not response.ok:
            raise GetContentException(f"Error downloading file from {order_path}", response.status_code)
    
        # read the content of the file
        content = response.content
        logging.info("Downloaded file from %s", order_path)
    else:
        # file is a local path 
        path = pathlib.Path(order_path)
        if not path.exists():
            raise ValueError(f"File {order_path} does not exist")
        
        if not path.is_file():
            raise ValueError(f"Path {order_path} is not a file")
        
        content = path.read_bytes()
        
    return content

class Client():

    def __init__(self, bucket_name, lambda_name):
        self.bucket_name = bucket_name
        self.lambda_name = lambda_name

    def extract(self, order_path: str | pathlib.Path, parts=("positions",), formats=("html",)):
        # check if parts and are tuples 
        if not isinstance(parts, tuple):
            raise ValueError("parts must be a tuple")
        if not isinstance(formats, tuple):
            raise ValueError("formats must be a tuple")
        
        # check if parts and formats are valid
        for part in parts:
            if part not in ("positions", "header"):
                raise ValueError(f"Invalid part: {part}")
            
        for format_value in formats:
            if format_value not in ("html", "json"):
                raise ValueError(f"Invalid format: {format_value}")
        
        try:
            content = _get_content(order_path)
        except GetContentException as e:
            return {
                "message": f"couldn't get the content from the provided url. The return statuscode was {e.status_code}",
                "status_code": 401
            }
        
        order_key = _upload_document(content, self.bucket_name)
        result = _get_extraction_result(order_key, self.lambda_name)
        output = _load_result_from_s3(result, self.bucket_name, parts=parts, formats=formats)

        object_key = "positions_html"
        if object_key in output:
            return {
                "message": "Extraction successful",
                "status_code": 200,
                "content": output[object_key]
            }
        else:
            return {
                "message": "Extraction failed",
                "status_code": 400
            }



