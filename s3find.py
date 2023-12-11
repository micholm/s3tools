import argparse
import boto3
import os
from urllib.parse import urlparse

argparser = argparse.ArgumentParser(
    prog="s3find", 
    description="recursivly searches from an s3 uri and returns full-formed s3 uri's if search term is found.")

argparser.add_argument("url", type=str, help="root url to use")
argparser.add_argument("string", type=str, help="search string")
argparser.add_argument("--extension", action="store_true", help="use if search string is a file extension")
argparser.add_argument("--no-count", action="store_true", help="do not print count, useful for programmatic return")

def is_s3(url):
    s3_url = urlparse(url, allow_fragments=False)
    return s3_url.scheme == "s3"

def get_registry(client:boto3.client, bucket:str, key:str, searchstring:str, extension:bool) -> [str]:
    r = []
    paginator = client.get_paginator('list_objects')
    response_iterator = paginator.paginate(Bucket=bucket, Prefix=key)

    for response in response_iterator:
        for object_data in response['Contents']:
            key = object_data['Key']
            if extension:
                if key.endswith(searchstring):
                    r.append(key)
            else:
                if key.find(searchstring):
                    r.append(key)
    return r

if __name__ == "__main__":
    args = argparser.parse_args()
    
    url = args.url
    searchstr = args.string
    isext = args.extension
    nocount = args.no_count

    try:
        s3_client = boto3.client('s3', endpoint_url=os.environ.get("AWS_ENDPOINT_URL_S3"))
        urlbit = urlparse(url, allow_fragments=False)
        r = get_registry(s3_client, urlbit.netloc, urlbit.path[1:-1], searchstr, isext)
        for line in r:
            print(f"{urlbit.scheme}://{urlbit.netloc}/{line}")
        if not nocount:
            print(f"returned: {len(r)}")
        exit(0)
    except Exception as ex:
        print(ex)
        exit(1)
    
