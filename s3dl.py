import argparse
import boto3
import os
from random import shuffle

from s3tools.s3 import S3Location
from s3tools.common import SharedProgram

prog = SharedProgram(
    "s3dl",
    "download a set of files based on recursive search")

prog.args.add_argument(
    "--out", 
    type=str, 
    help="download location", 
    default=os.getcwd())

if __name__ == "__main__":
    args = prog.parse_args()
    prog.print_preamble()

    s3_client = boto3.client('s3', endpoint_url=os.environ.get("AWS_ENDPOINT_URL_S3"))

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