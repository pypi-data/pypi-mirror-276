import base64
import hashlib
import hmac
import time
import typing
from urllib.parse import urlparse

import httpx
from httpx import BaseTransport, Limits, URL
from httpx._client import EventHook
from httpx._config import DEFAULT_TIMEOUT_CONFIG, DEFAULT_LIMITS, DEFAULT_MAX_REDIRECTS
from httpx._types import AuthTypes, QueryParamTypes, HeaderTypes, CookieTypes, VerifyTypes, CertTypes, ProxyTypes, \
    ProxiesTypes, TimeoutTypes, URLTypes


class NcloudClient(httpx.Client):
    def __init__(self, *, auth: AuthTypes | None = None, params: QueryParamTypes | None = None,
                 headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, verify: VerifyTypes = True,
                 cert: CertTypes | None = None, http1: bool = True, http2: bool = False,
                 proxy: ProxyTypes | None = None, proxies: ProxiesTypes | None = None,
                 mounts: None | (typing.Mapping[str, BaseTransport | None]) = None,
                 timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG, follow_redirects: bool = False,
                 limits: Limits = DEFAULT_LIMITS, max_redirects: int = DEFAULT_MAX_REDIRECTS,
                 event_hooks: None | (typing.Mapping[str, list[EventHook]]) = None, base_url: URLTypes = "",
                 transport: BaseTransport | None = None, app: typing.Callable[..., typing.Any] | None = None,
                 trust_env: bool = True, default_encoding: str | typing.Callable[[bytes], str] = "utf-8",
                 access_key: str, secret_key: str, ) -> None:
        super().__init__(auth=auth, params=params, headers=headers, cookies=cookies, verify=verify, cert=cert,
                         http1=http1, http2=http2, proxy=proxy, proxies=proxies, mounts=mounts, timeout=timeout,
                         follow_redirects=follow_redirects, limits=limits, max_redirects=max_redirects,
                         event_hooks=event_hooks, base_url=base_url, transport=transport, app=app, trust_env=trust_env,
                         default_encoding=default_encoding)
        self.access_key = access_key
        self.secret_key = secret_key

    def request(self, method, url, **kwargs):
        modified_url = f"{self.base_url}{url}"
        timestamp = str(int(time.time() * 1000))
        params = kwargs.get("params", {})

        params = self._merge_queryparams(params)
        url_obj = URL(url)
        url_obj = url_obj.copy_merge_params(params=params)
        parsed_url = urlparse(str(url_obj))
        path_and_query = f"{parsed_url.path}?{parsed_url.query}"

        signature = self.create_signature(method, path_and_query, timestamp)

        update_headers: HeaderTypes = {
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-apigw-signature-v2": signature,
        }

        kwargs['headers'] = {**(kwargs.get('headers') or {}), **update_headers}

        return super(NcloudClient, self).request(method=method, url=modified_url, **kwargs, )

    def create_signature(self, method, uri, timestamp):
        secret_key_byte = bytes(self.secret_key, 'UTF_8')

        message = method + " " + uri + "\n" + timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')

        return base64.b64encode(hmac.new(secret_key_byte, message, digestmod=hashlib.sha256).digest())
