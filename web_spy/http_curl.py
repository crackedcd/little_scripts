#!/usr/bin/python

import requests # pip install requests
import sys

class HTTP_CURL:
    '''curl request spy.'''
    
    def __init__(self, url, timeout, chk_str = '|OK|', postdata = None):
        '''initializes curl content.'''
        self.url = url
        self.timeout = float(timeout)
        self.postdata = postdata
        self.chk_str = chk_str

    def __del__(self):
        '''free resources.'''

    def curl_timeout(self):
        try:
            r = requests.get(self.url, timeout=self.timeout)
        except requests.exceptions.Timeout as err:
            print("request time out: ", err)
            return False
        except requests.exceptions.ConnectionError as err:
            print("connection failed: ", err)
            return False

    def curl_get_content(self):
        if self.curl_timeout() == False:
            return False
        else:
            if self.postdata == None:
                    r = requests.get(self.url)
                    return r.content
            else:
                    r = requests.post(self.url, data=self.postdata)
                    return r.content
    def http_spy(self):
        if self.curl_get_content() == False:
            pass
        else:
            #
            # bytes to str
            # str(b, encoding = "utf-8") 
            # or bytes.decode(b)
            #
            # str to bytes
            # bytes(s, encoding = "utf8")
            # or str.encode(s)
            #
            c = bytes.decode(self.curl_get_content())
            if self.chk_str in c:
                print('y')
            else:
                print('n')
 

