from enum import Enum, auto
import ssl

from typing import Any, Dict, Iterable, Optional, Union
import importlib.resources as pkg_resources

import chardet
from httpx import Client
import httpx
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager  # type: ignore

from . import _certificate
from urllib3 import Retry as __retry__

import importlib.metadata
version = importlib.metadata.version('tuyul_sdk')

DEFAULT_CIPHERS = ":".join(
    [
        "ECDHE+AESGCM",
        "ECDHE+CHACHA20",
        "DHE+AESGCM",
        "DHE+CHACHA20",
        "ECDH+AESGCM",
        "DH+AESGCM",
        "ECDH+AES",
        "DH+AES",
        "RSA+AESGCM",
        "RSA+AES",
        "!aNULL",
        "!eNULL",
        "!MD5",
        "!DSS",
    ]
)

MY_CHIPER = ':'.join(
    [
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384",
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-CHACHA20-POLY1305",
        "ECDHE-RSA-CHACHA20-POLY1305",
        "DHE-RSA-AES256-GCM-SHA384",
        "DHE-RSA-AES128-GCM-SHA256",
        "DHE-RSA-CHACHA20-POLY1305",
        "ECDHE-ECDSA-AES256-CCM8",
        "ECDHE-ECDSA-AES256-CCM",
        "ECDHE-ECDSA-AES128-CCM8",
        "ECDHE-ECDSA-AES128-CCM",
        "ECDHE-ECDSA-AES256-SHA384",
        "ECDHE-RSA-AES256-SHA384",
        "ECDHE-ECDSA-AES128-SHA256",
        "ECDHE-RSA-AES128-SHA256",
        "ECDHE-ECDSA-AES256-SHA",
        "ECDHE-RSA-AES256-SHA",
        "ECDHE-ECDSA-AES128-SHA",
        "ECDHE-RSA-AES128-SHA",
        "DHE-RSA-AES256-CCM8",
        "DHE-RSA-AES256-CCM",
        "DHE-RSA-AES128-CCM8",
        "DHE-RSA-AES128-CCM",
        "DHE-RSA-AES256-SHA256",
        "DHE-RSA-AES128-SHA256",
        "DHE-RSA-AES256-SHA",
        "DHE-RSA-AES128-SHA",
        "AES256-GCM-SHA384",
        "AES128-GCM-SHA256",
        "AES256-CCM8",
        "AES256-CCM",
        "AES128-CCM8",
        "AES128-CCM",
        "AES256-SHA256",
        "AES128-SHA256",
        "AES256-SHA",
        "AES128-SHA",
        'RC4-SHA'
    ]
)

class SSLContext(ssl.SSLContext):
    """SSLContext wrapper."""

    def set_alpn_protocols(self, alpn_protocols: Iterable[str]) -> None:
        """
        ALPN headers cause Google to return 403 Bad Authentication.
        """

def certificate():
    with pkg_resources.path(_certificate, 'cacert.pem') as p:
        return str(p)

class Retry:

    def __new__(cls) -> '__retry__':
        return __retry__(
            total=3,
            status_forcelist=[104, 429, 500, 502, 503, 504],
            backoff_factor=2
        )

class RequestsAdapter(HTTPAdapter):
    
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        if "timeout" in kwargs:
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)
    
    """TLS tweaks."""

    def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
        """
        Secure settings from ssl.create_default_context(), but without
        ssl.OP_NO_TICKET which causes Google to return 403 Bad
        Authentication.
        """
        context = SSLContext()
        context.set_ciphers(MY_CHIPER)
        #context.set_alpn_protocols(ssl.PROTOCOL_SSLv23)
        #context.verify_mode = ssl.CERT_REQUIRED
        context.options &= ~ssl.OP_NO_TICKET  # pylint: disable=E1101
        self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)

class TypeInjector(Enum):

    requests = auto()
    httpx = auto()

class ProxyType(Enum):
    
    socks5  = auto()
    http    = auto()

class ProxyParams:

    URL: str = None

    def __new__(cls, type: ProxyType, IP: str, PORT: int, USERNAME: Optional[str] = None, PASSWORD: Optional[str] = None) -> 'ProxyParams':
        if USERNAME is not None and PASSWORD is not None:
            build = f'{USERNAME}:{PASSWORD}@{IP}:{PORT}'
        else:
            build = f'{IP}:{PORT}'
        if type == ProxyType.http:
            setattr(ProxyParams, 'URL', f'http://{build}')
        elif type == ProxyType.socks5:
            setattr(ProxyParams, 'URL', f'socks5://{build}')
        return cls

class HClient:

    @staticmethod
    def __autodetect__(content):
        return chardet.detect(content).get('encoding')
    
    def __new__(cls, timeout: int, headers: Dict[str, str], proxy_url: Optional[str] = None) -> Client:
        context = SSLContext()
        context.set_ciphers(MY_CHIPER)
        context.options &= ~ssl.OP_NO_TICKET  # pylint: disable=E1101
        context.load_verify_locations(cafile=certificate())
        timeouts    = httpx.Timeout(float(timeout), connect=60.0)
        transport   = httpx.HTTPTransport(http2=True, retries=3.0)
        header: Dict[str, str] = dict()
        try:
            for k, v in zip(headers.keys(), headers.values()): header.update(**{k.lower():v})
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        except AttributeError:
            header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        return httpx.Client(http2=True, cert=context, verify=context, proxies=proxy_url, headers=header, default_encoding=cls.__autodetect__, timeout=timeouts, transport=transport)

class RClient:

    def __new__(cls, timeout: int, headers: Dict[str, str], proxy_url: Optional[str] = None) -> 'Session':
        requests = Session()
        adapter = RequestsAdapter(timeout=timeout, max_retries=Retry)
        for scheme in ('http://', 'https://'): requests.mount(scheme, adapter)
        if not proxy_url:
            requests.proxies = dict()
        else:
            requests.proxies = dict(http = proxy_url, https = proxy_url)

        header: Dict[str, str] = dict()
        try:
            for k, v in zip(headers.keys(), headers.values()): header.update(**{k.lower():v})
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        except AttributeError:
            header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        requests.headers.update(**header)
        return requests

class Connections(HClient, RClient):

    def __new__(cls, typeInjector: TypeInjector, timeout: int = 30, extra_headers: Dict[str, str] = dict(), proxyParams: Optional[ProxyParams] = None) -> Union[Client, Session]:
        if not proxyParams: proxy_url = None
        else:
            proxy_url = proxyParams.URL
        if typeInjector == TypeInjector.requests:
            return RClient.__new__(cls, timeout, extra_headers, proxy_url)
        elif typeInjector == TypeInjector.httpx:
            return HClient.__new__(cls, timeout, extra_headers, proxy_url)
    
