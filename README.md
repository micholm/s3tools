# s3tools

### usage

```
# download all jpgs in bucket
python s3dl.py s3://<bucket> jpg --extension
```

```
# download a random sample of jpgs in bucket, ignoring a subfolder
python s3dl.py \
    s3://<bucket> \
    jpg \
    --extension \
    --randomise-result \
    --randomise-result-count 100 \
    --ignore-keyword failed
```