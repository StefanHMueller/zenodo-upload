# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 15:28:32 2022

@author: smueller
"""

import io
import requests
from typing import Union
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
import os



class UploadChunksIterator():
    """
    This is an interface between python requests and tqdm.
    Make tqdm to be accessed just like IOBase for requests lib.
    """

    def __init__(
        self, file: Union[io.BufferedReader, CallbackIOWrapper], total_size: int, chunk_size: int = 16 * 1024
    ):  # 16MiB
        self.file = file
        self.chunk_size = chunk_size
        self.total_size = total_size

    def __iter__(self):
        return self

    def __next__(self):
        data = self.file.read(self.chunk_size)
        if not data:
            raise StopIteration
        return data

    # we dont retrive len from io.BufferedReader because CallbackIOWrapper only has read() method.
    def __len__(self):
        return self.total_size

folder = 'D:/NAR_upload/Mueller_et_al_NAR/zips/'
files = os.listdir(folder)

with open('token.txt') as f:
    token = f.readline()
    
ACCESS_TOKEN = token
#%%
upload_url = "https://zenodo.org/api/deposit/depositions/7042235"

r = requests.get(upload_url, params={'access_token': ACCESS_TOKEN})

bucket_url = r.json()["links"]["bucket"]

_quiet = False
        
index = 0
success = 0
while success < len(files):
    try:
        s3url = bucket_url + '/' + files[index]
        with open(folder+files[index], "rb") as f:
            total_size = os.fstat(f.fileno()).st_size
            if not _quiet:
                f = tqdm.wrapattr(f, "read", miniters=1, total=total_size, ascii=True)

            with f as f_iter:
                res = requests.put(
                    url=s3url,
                    data=UploadChunksIterator(f_iter, total_size=total_size),
                    params = {'access_token': ACCESS_TOKEN},
                    headers = {"Connection": "keep-alive"},
                    )
            res.raise_for_status()
        print("succesfully uploaded {}, {} files to go.".format(files[index],len(files)-1-index))
        index += 1
        success += 1      
    except Exception as e:
        print(e)
        
    
    
    
    