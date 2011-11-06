'''\
The Httplib2 clinet

This is a thin layer on top of httplib2 python library.

http://code.google.com/p/httplib2/
'''
import httplib2


from .std import HttpClientHandler, HttpClientResponse, to_bytestring,\
                    HTTPError, URLError


class Response(HttpClientResponse):

    def __init__(self, response, content = None):
        self._resp = response
        self.status_code = getattr(response, 'status', None)
        self.content = content
        response.pop('status',None)
        self.headers = response
        self.url = getattr(response, 'url', None)

    
class HttpClient2(HttpClientHandler):
    type = 2
    def __init__(self, proxy_info = None,
                 timeout = None, cache = None,
                 headers = None, handle_cookie = False):
        self._opener = httplib2.Http(cache = cache,
                                     timeout = timeout,
                                     proxy_info = proxy_info)
        self.headers = dict(self.get_headers(headers))
        
    @property
    def timeout(self):
        return self._opener.timeout
    
    def request(self, uri, body=None, method='GET', **kwargs):
        if body:
            body = to_bytestring(body)
        try:
            r,c = self._opener.request(uri,
                                       method=method,
                                       body=body,
                                       headers=self.headers)
        except (HTTPError,URLError) as why:
            return Response(why)
        else:
            return Response(r,c)
    
    def add_credentials(self, username, password, domain = ''):
        self._opener.add_credentials(username, password, domain)

