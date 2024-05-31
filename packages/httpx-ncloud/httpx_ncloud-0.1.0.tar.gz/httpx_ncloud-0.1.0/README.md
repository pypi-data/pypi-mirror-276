# httpx-ncloud
## Intro
__httpx-ncloud__ is a library that automatically generates a signature key for "httpx". 
This library is designed to make requests to the Ncloud API more convenient.

## how to use
```python
from httpx_ncloud import NcloudClient

client = NcloudClient(base_url="https://cloudsearch.apigw.ntruss.com",
                      access_key="a", secret_key="b", )
res = client.get(url="/v1/domain/rel-20240509")
```