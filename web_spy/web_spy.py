#!/usr/bin/python

import http_curl
import types

# DEFINE 
HTTP_CURL_TIMEOUT = ('0.05')

url = "http://121.199.25.184:88/1.php"
post = {
'a':'1',
'b':'2',
}
u = http_curl.HTTP_CURL(url, HTTP_CURL_TIMEOUT, '222', post)
u.http_spy()

url = "http://121.199.25.184:88/2.php"
u = http_curl.HTTP_CURL(url, HTTP_CURL_TIMEOUT)
u.http_spy()

url = "http://121.199.25.184:88/2.php"
u = http_curl.HTTP_CURL(url, HTTP_CURL_TIMEOUT, "static")
u.http_spy()

url = "http://www.sandiecomo.com"
u = http_curl.HTTP_CURL(url, HTTP_CURL_TIMEOUT)
u.http_spy()

url = "http://www.abcxyzccc.com"
u = http_curl.HTTP_CURL(url, HTTP_CURL_TIMEOUT)
u.http_spy()
