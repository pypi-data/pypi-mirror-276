# pylint:disable-msg=W1401
"""
Unit tests for download functions from the trafilatura library.
"""

import gzip
import logging
import os
import sys
import zlib

try:
    import pycurl
    HAS_PYCURL = True
except ImportError:
    HAS_PYCURL = False

try:
    import brotli
    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False

try:
    import zstandard
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

from time import sleep
from unittest.mock import patch

import pytest

from courlan import UrlStore

from trafilatura.cli import parse_args
from trafilatura.cli_utils import (download_queue_processing,
                                   url_processing_pipeline)
from trafilatura.core import Extractor, extract
import trafilatura.downloads
from trafilatura.downloads import (DEFAULT_HEADERS, USER_AGENT, Response,
                                   _determine_headers, _handle_response,
                                   _parse_config, _pycurl_is_live_page,
                                   _send_pycurl_request, _send_urllib_request,
                                   _urllib3_is_live_page,
                                   add_to_compressed_dict, fetch_url,
                                   is_live_page, load_download_buffer)
from trafilatura.settings import DEFAULT_CONFIG, args_to_extractor, use_config
from trafilatura.utils import decode_file, decode_response, handle_compressed_file, load_html

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ZERO_CONFIG = DEFAULT_CONFIG
ZERO_CONFIG['DEFAULT']['MIN_OUTPUT_SIZE'] = '0'
ZERO_CONFIG['DEFAULT']['MIN_EXTRACTED_SIZE'] = '0'

RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')
UA_CONFIG = use_config(filename=os.path.join(RESOURCES_DIR, 'newsettings.cfg'))

DEFAULT_OPTS = Extractor(config=DEFAULT_CONFIG)


def _reset_downloads_global_objects():
    """
    Force global objects to be re-created
    """
    trafilatura.downloads.HTTP_POOL = None
    trafilatura.downloads.NO_CERT_POOL = None
    trafilatura.downloads.RETRY_STRATEGY = None


def test_response_object():
    "Test if the Response class is functioning as expected."
    my_html = b"<html><body><p>ABC</p></body></html>"
    resp = Response(my_html, 200, "https://example.org")
    assert bool(resp) is True
    resp.store_headers({"X-Header": "xyz"})
    assert "x-header" in resp.headers
    resp.decode_data(True)
    assert my_html.decode("utf-8") == resp.html == str(resp)
    my_dict = resp.as_dict()
    assert sorted(my_dict) == ["data", "headers", "html", "status", "url"]


def test_fetch():
    '''Test URL fetching.'''
    # sanity check
    assert _send_urllib_request('', True, False, DEFAULT_CONFIG) is None
    with pytest.raises(ValueError):
        fetch_url("https://example.org", decode=False)

    # is_live general tests
    assert _urllib3_is_live_page('https://httpbun.com/status/301') is True
    assert _urllib3_is_live_page('https://httpbun.com/status/404') is False
    assert is_live_page('https://httpbun.com/status/403') is False
    # is_live pycurl tests
    if HAS_PYCURL:
        assert _pycurl_is_live_page('https://httpbun.com/status/301') is True

    # fetch_url
    assert fetch_url('#@1234') is None
    assert fetch_url('https://httpbun.com/status/404') is None
    # test if the functions default to no_ssl
    # doesn't work?
    # assert _send_urllib_request('https://expired.badssl.com/', False, False, DEFAULT_CONFIG) is not None
    if HAS_PYCURL:
        assert _send_pycurl_request('https://expired.badssl.com/', False, False, DEFAULT_CONFIG) is not None
    # no SSL, no decoding
    url = 'https://httpbun.com/status/200'
    for no_ssl in (True, False):
        response = _send_urllib_request('https://httpbun.com/status/200', no_ssl, True, DEFAULT_CONFIG)
        assert b"200" in response.data and b"OK" in response.data  # JSON
        assert response.headers["x-powered-by"].startswith("httpbun")
    if HAS_PYCURL:
        response1 = _send_pycurl_request('https://httpbun.com/status/200', True, True, DEFAULT_CONFIG)
        assert response1.headers["x-powered-by"].startswith("httpbun")
        assert _handle_response(url, response1, False, DEFAULT_OPTS).data == _handle_response(url, response, False, DEFAULT_OPTS).data
        assert _handle_response(url, response1, True, DEFAULT_OPTS) == _handle_response(url, response, True, DEFAULT_OPTS)
    # response object
    # too large response object
    data = ""
    status = 200
    url = 'https://httpbin.org/encoding/utf8'
    response = Response(data, status, url)
    # too large
    response.data = b'ABC'*10000000
    assert _handle_response(response.url, response, False, DEFAULT_OPTS) is None
    # too small
    response.data = b'ABC'
    assert _handle_response(response.url, response, False, DEFAULT_OPTS) is None
    # straight handling of response object
    with open(os.path.join(RESOURCES_DIR, 'utf8.html'), 'rb') as filehandle:
        response.data = filehandle.read()
    assert _handle_response(response.url, response, False, DEFAULT_OPTS) is not None
    assert load_html(response) is not None
    # nothing to see here
    assert extract(response, url=response.url, config=ZERO_CONFIG) is None
    # test handling redirects
    res = fetch_url('https://httpbun.com/redirect/2')
    assert len(res) > 100  # We followed redirects and downloaded something in the end
    new_config = use_config()  # get a new config instance to avoid mutating the default one
    # Patch max directs: limit to 0. We won't fetch any page as a result
    new_config.set('DEFAULT', 'MAX_REDIRECTS', '0')
    _reset_downloads_global_objects()  # force Retry strategy and PoolManager to be recreated with the new config value
    res = fetch_url('https://httpbun.com/redirect/1', config=new_config)
    assert res is None
    # Also test max redir implementation on pycurl if available
    if HAS_PYCURL:
        assert _send_pycurl_request('https://httpbun.com/redirect/1', True, False, new_config) is None
    _reset_downloads_global_objects()  # reset global objects again to avoid affecting other tests


def test_config():
    '''Test how configuration options are read and stored.'''
    # default config is none
    assert _parse_config(DEFAULT_CONFIG) == (None, None)
    # default accept-encoding
    accepted = ['deflate', 'gzip']
    if HAS_BROTLI:
        accepted.append('br')
    if HAS_ZSTD:
        accepted.append('zstd')
    assert sorted(DEFAULT_HEADERS['accept-encoding'].split(',')) == sorted(accepted)
    # default user-agent
    default = _determine_headers(DEFAULT_CONFIG)
    assert default['User-Agent'] == USER_AGENT
    assert 'Cookie' not in default
    # user-agents rotation
    assert _parse_config(UA_CONFIG) == (['Firefox', 'Chrome'], 'yummy_cookie=choco; tasty_cookie=strawberry')
    custom = _determine_headers(UA_CONFIG)
    assert custom['User-Agent'] in ['Chrome', 'Firefox']
    assert custom['Cookie'] == 'yummy_cookie=choco; tasty_cookie=strawberry'


def test_decode():
    '''Test how responses are being decoded.'''
    html_string = "<html><head/><body><div>ABC</div></body></html>"
    # response type
    assert decode_file(b" ") is not None
    # GZip
    gz_string = gzip.compress(html_string.encode("utf-8"))
    assert handle_compressed_file(gz_string) == html_string.encode("utf-8")
    assert decode_file(gz_string) == html_string
    with pytest.raises(ValueError):
        decode_response(gz_string)
    # Deflate
    deflate_string = zlib.compress(html_string.encode("utf-8"))
    assert handle_compressed_file(deflate_string) == html_string.encode("utf-8")
    assert decode_file(deflate_string) == html_string
    # Brotli
    if HAS_BROTLI:
        brotli_string = brotli.compress(html_string.encode("utf-8"))
        assert handle_compressed_file(brotli_string) == html_string.encode("utf-8")
        assert decode_file(brotli_string) == html_string
    # ZStandard
    if HAS_ZSTD:
        zstd_string = zstandard.compress(html_string.encode("utf-8"))
        assert handle_compressed_file(zstd_string) == html_string.encode("utf-8")
        assert decode_file(zstd_string) == html_string
    # errors
    for bad_file in ("äöüß", b"\x1f\x8b\x08abc", b"\x28\xb5\x2f\xfdabc"):
        assert handle_compressed_file(bad_file) == bad_file


def test_queue():
    'Test creation, modification and download of URL queues.'
    # test conversion and storage
    url_store = add_to_compressed_dict(['ftps://www.example.org/', 'http://'])
    assert isinstance(url_store, UrlStore)
    # download buffer
    inputurls = ['https://test.org/1', 'https://test.org/2', 'https://test.org/3', 'https://test2.org/1', 'https://test2.org/2', 'https://test2.org/3', 'https://test3.org/1', 'https://test3.org/2', 'https://test3.org/3', 'https://test4.org/1', 'https://test4.org/2', 'https://test4.org/3', 'https://test5.org/1', 'https://test5.org/2', 'https://test5.org/3', 'https://test6.org/1', 'https://test6.org/2', 'https://test6.org/3']
    url_store = add_to_compressed_dict(inputurls)
    bufferlist, _ = load_download_buffer(url_store, sleep_time=5)
    assert len(bufferlist) == 6
    sleep(0.25)
    bufferlist, _ = load_download_buffer(url_store, sleep_time=0.1)
    assert len(bufferlist) == 6
    # CLI args
    url_store = add_to_compressed_dict(['https://www.example.org/'])
    testargs = ['', '--list']
    with patch.object(sys, 'argv', testargs):
        args = parse_args(testargs)
    assert url_processing_pipeline(args, url_store) is False
    # single/multiprocessing
    testargs = ['', '-v']
    with patch.object(sys, 'argv', testargs):
        args = parse_args(testargs)
    inputurls = ['https://httpbun.com/status/301', 'https://httpbun.com/status/304', 'https://httpbun.com/status/200', 'https://httpbun.com/status/300', 'https://httpbun.com/status/400', 'https://httpbun.com/status/505']
    url_store = add_to_compressed_dict(inputurls)
    args.archived = True
    args.config_file = os.path.join(RESOURCES_DIR, 'newsettings.cfg')
    options = args_to_extractor(args)
    options.config['DEFAULT']['SLEEP_TIME'] = '0.2'
    results = download_queue_processing(url_store, args, None, options)
    assert len(results[0]) == 5 and results[1] is None


if __name__ == '__main__':
    test_response_object()
    test_fetch()
    test_config()
    test_decode()
    test_queue()
