from typing import List
import boto3
from urllib.parse import urlparse

class S3Location:
    def __init__(self, url:str) -> None:
        urlbit = urlparse(url, allow_fragments=False)
        self.scheme = urlbit.scheme

        if not self.is_s3():
            raise Exception(f"not a valid s3 url: {url}")
        
        self.bucket = urlbit.netloc
        self.key = urlbit.path[1:0]

    def get_formed_url(self)->str:
        return f"{self.scheme}://{self.bucket}{self.key}"
    
    def __str__(self) -> str:
        return self.get_formed_url()
        
    def is_s3(self):
        return self.scheme == 's3'
    
    def find_recursive(self, client:boto3.client, searchstring:str, extension:bool=False, ignore_keyword=None, verbose=False) -> List[str]:
        r = []
        paginator = client.get_paginator('list_objects')
        response_iterator = paginator.paginate(Bucket=self.bucket, Prefix=self.key)

        for response in response_iterator:
            for object_data in response['Contents']:
                key = object_data['Key']
                store = False

                if extension:
                    if key.endswith(searchstring):
                        store = True
                else:
                    if key.find(searchstring) >= 0:
                        store = True
                
                if ignore_keyword is not None and key.find(ignore_keyword) >= 0:
                    store = False
                
                if store:
                    r.append([self.bucket, f"{self.key}{key}"])
                elif verbose:
                    print(f"ignoring key: {key}")
        return r

# def get_registry(client:boto3.client, s3path:S3Location, searchstring:str, extension:bool) -> List[str]:
#     r = []
#     paginator = client.get_paginator('list_objects')
#     response_iterator = paginator.paginate(Bucket=s3path.bucket, Prefix=s3path.key)

#     for response in response_iterator:
#         for object_data in response['Contents']:
#             key = object_data['Key']
#             if extension:
#                 if key.endswith(searchstring):
#                     r.append(key)
#             else:
#                 if key.find(searchstring):
#                     r.append(key)
#     return r