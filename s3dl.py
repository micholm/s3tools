import argparse
import boto3
import os
from random import shuffle

from s3tools.s3 import S3Location

argparser = argparse.ArgumentParser(
    prog="s3dl", 
    description="download a set of files based on recursive search")

argparser.add_argument("url", type=str, help="root url to use")
argparser.add_argument("string", type=str, help="search string")
argparser.add_argument("--out", type=str, help="download location", default=os.getcwd())
argparser.add_argument("--extension", action="store_true", help="use if search string is a file extension")
argparser.add_argument("--ignore-keyword", help="will ignore any path containing this keyword")
argparser.add_argument("--ignore-case", action="store_true", help="ignore case for seach and ignore terms")
argparser.add_argument("--randomise-result", action="store_true", help="if true, list of results found will be in randomised order")
argparser.add_argument("--randomise-result-count", type=int, default=-1, help="how many results to collect from randomised list. -1 for whole list")

if __name__ == "__main__":
    s3_client = boto3.client('s3', endpoint_url=os.environ.get("AWS_ENDPOINT_URL_S3"))
    args = argparser.parse_args()

    loc = S3Location(args.url)
    r = loc.find_recursive(s3_client, 
                           args.string, 
                           args.extension, 
                           ignore_keyword=args.ignore_keyword, 
                           ignore_case=args.ignore_case)

    i = len(r)
    if args.randomise_result:
        shuffle(r)
        if args.randomise_result_count > 0:
            i = args.randomise_result_count

    os.makedirs(args.out, exist_ok=True)
    print(f"downloading {i}/{len(r)} files")
    while i > 0:
        i -= 1
        print(f"[{i+1}] -> {r[i][0]}/{r[i][1]}")
        s3_client.download_file(r[i][0], r[i][1], os.path.join(args.out, os.path.basename(r[i][1])))
        

    
