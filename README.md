# s3tools

### usage

## s3dl.py
```
usage: s3dl [-h] [--out OUT] [--extension] [--ignore-keyword IGNORE_KEYWORD] [--ignore-case] [--randomise-result]
            [--randomise-result-count RANDOMISE_RESULT_COUNT]
            url string

download a set of files based on recursive search

positional arguments:
  url                   root url to use
  string                search string

options:
  -h, --help            show this help message and exit
  --out OUT             download location
  --extension           use if search string is a file extension
  --ignore-keyword IGNORE_KEYWORD
                        will ignore any path containing this keyword
  --ignore-case         ignore case for seach and ignore terms
  --randomise-result    if true, list of results found will be in randomised order
  --randomise-result-count RANDOMISE_RESULT_COUNT
                        how many results to collect from randomised list. -1 for whole list
```
### examples
```
# download all jpgs in bucket
python s3dl.py s3://<bucket> jpg --extension
```

```
# download a random sample of jpgs in bucket, ignoring ant paths with 'failed'
python s3dl.py \
    s3://<bucket> \
    jpg \
    --extension \
    --randomise-result \
    --randomise-result-count 100 \
    --ignore-keyword failed
```

```
# download a complete list of jpgs in bucket, ignoring case
python s3dl.py \
    s3://<bucket> \
    JPG \
    --extension \
    --ignore-case
```
## s3find.py
```
usage: s3find [-h] [--extension] [--ignore-keyword IGNORE_KEYWORD] [--no-count] [--ignore-case] url string

recursivly searches from an s3 uri and returns full-formed s3 uri's if search term is found.

positional arguments:
  url                   root url to use
  string                search string

options:
  -h, --help            show this help message and exit
  --extension           use if search string is a file extension
  --ignore-keyword IGNORE_KEYWORD
                        will ignore any path containing this keyword
  --no-count            do not print count, useful for programmatic return
  --ignore-case         ignore case for seach and ignore terms
```