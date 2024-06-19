import argparse
import boto3
import os
from urllib.parse import urlparse

from src.s3 import S3Location

argparser = argparse.ArgumentParser(
    prog="s3find", 
    description="recursivly searches from an s3 uri and returns full-formed s3 uri's if search term is found.")

argparser.add_argument("url", type=str, help="root url to use")
argparser.add_argument("string", type=str, help="search string")
argparser.add_argument("--extension", action="store_true", help="use if search string is a file extension")
argparser.add_argument("--no-count", action="store_true", help="do not print count, useful for programmatic return")

if __name__ == "__main__":
    args = argparser.parse_args()
    
    url = args.url
    searchstr = args.string
    isext = args.extension
    nocount = args.no_count

    try:
        s3_client = boto3.client('s3', endpoint_url=os.environ.get("AWS_ENDPOINT_URL_S3"))
        s3location = S3Location(url)

        # urlbit = urlparse(url, allow_fragments=False)
        r = s3location.find_recursive(s3_client, searchstr, isext)
        for line in r:
            print(r)
        if not nocount:
            print(f"returned: {len(r)}")
        exit(0)
    except Exception as ex:
        print(ex)
        exit(1)
    