# import argparse
import boto3
import os
from random import shuffle

from s3tools.s3 import S3Location
from s3tools.common import SharedProgram

prog = SharedProgram("s3find", 
                     "recursivly searches from an s3 uri and \
                      returns full-formed s3 uri's if search term is found.")

prog.args.add_argument(
    "--no-count", 
    action="store_true", 
    help="do not print count, useful for programmatic return")

if __name__ == "__main__":
    args = prog.parse_args()
    prog.print_preamble()

    url = args.url
    searchstr = args.string
    isext = args.extension
    nocount = args.no_count

    try:
        s3_client = boto3.client('s3', endpoint_url=os.environ.get("AWS_ENDPOINT_URL_S3"))
        s3location = S3Location(url)

        r = s3location.find_recursive(s3_client, searchstr, isext, 
                                      args.ignore_keyword, ignore_case=args.ignore_case)
        
        i = len(r)
        count = len(r)
        if args.randomise_result:
            shuffle(r)
            if args.randomise_result_count > 0:
                i = count = args.randomise_result_count

        while i > 0:
            i -= 1
            print(f"s3://{r[i][0]}/{r[i][1]}")
        if not nocount:
            if args.randomise_result_count > 0:
                print(f"returned {count}/{len(r)}")
            else:
                print(f"returned: {count}")
        exit(0)
    except Exception as ex:
        print(ex)
        exit(1)
    
