# zenodo-upload
upload big files to Zenodo.org using python

Uploading big files to https://zenodo.org using poython.

Inspired by this stackExchange discussion: https://stackoverflow.com/questions/13909900/progress-of-python-requests-post

# prerequisites

1. Python
2. requests 
3. tdqm

# usage

1. create a new upload in Zenodo using the web ui and click ```save```
2. copy the depositions url id e.g. ```https://zenodo.org/deposit/depositions/12345``` and set it in the scipt (``upload_url=...``)
3. copy your access token (see https://zenodo.org/account/settings/applications/tokens/new/)
4. save all files to upload i a folder, set ``folder="path/to/your/folder/``
5.run the script. you should see something like this: ``100%|##########| 3.17G/3.17G [28:11<00:00, 2.01MB/s] ``
6. go back to the web ui to finalize and publish your upload.

good luck!
 



