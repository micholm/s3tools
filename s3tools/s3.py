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
        self.key = urlbit.path[1:]

    def get_formed_url(self)->str:
        return f"{self.scheme}://{self.bucket}{self.key}"
    
    def __str__(self) -> str:
        return self.get_formed_url()
        
    def is_s3(self):
        return self.scheme == 's3'
    
    def find_recursive(self, 
                       client:boto3.client, 
                       searchstring:str, 
                       extension:bool=False, 
                       ignore_keyword=None, 
                       verbose=False,
                       ignore_case=True) -> List[str]:
        
        def keymatch(path, key, ext, case_insensitive, ignore):
            res = False
            p = path.lower() if case_insensitive else path
            k = key.lower() if case_insensitive else key
            ig = ignore.lower() if ignore is not None and case_insensitive else ignore
            if ext:
                if p.endswith(k):
                    res = True
            else:
                if p.find(k) >= 0:
                    res = True
            if ig is not None and p.find(ig) >= 0:
                res = False
            return res
        
        r = []
        paginator = client.get_paginator('list_objects')
        response_iterator = paginator.paginate(Bucket=self.bucket, Prefix=self.key)

        for response in response_iterator:
            for object_data in response['Contents']:
                key = object_data['Key']

                if keymatch(key, searchstring, extension, ignore_case, ignore_keyword):
                    r.append([self.bucket, key])
                elif verbose:
                    print(f"ignoring key: {key}")
        return r