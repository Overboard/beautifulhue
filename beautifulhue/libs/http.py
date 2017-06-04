import json
# For Python 2, urllib2 will import
try:
    import urllib
    import urllib2

    class Request:

        def _request(self, url, data, action, content_type):

            if ((data or isinstance(data, dict)) and
                action not in ('GET', 'DELETE',)):
                data = json.dumps(data)
                if action == 'PUT':
                    opener = urllib2.build_opener(urllib2.HTTPHandler)
                    req = urllib2.Request(url, data=data)
                    req.add_header('Content-Type', content_type)
                    req.get_method = lambda: 'PUT'
                    conn = opener.open(req)
                else:
                    headers = {'Content-Type': content_type}
                    try:
                        req = urllib2.Request(url, data, headers)
                        conn = urllib2.urlopen(req)
                    except TypeError:
                        # This is for the _lights.find bodyless POST.
                        data = urllib.urlencode(data, 1)
                        req = urllib2.Request(url, data, headers)
                        conn = urllib2.urlopen(req)
            elif action == 'DELETE':
                opener = urllib2.build_opener(urllib2.HTTPHandler)
                req = urllib2.Request(url)
                req.get_method = lambda: 'DELETE'
                conn = opener.open(req)
            else:
                req = urllib2.Request(url)
                conn = urllib2.urlopen(req)
            response = conn.read()
            conn.close()
            try:
                content = json.loads(response)
            except:
                content = response
            return conn.info().headers, content

        def get(self, url, data=None, content_type='application/json'):
            return self._request(url, data, 'GET', content_type)

        def post(self, url, data={}, content_type='application/json'):
            return self._request(url, data, 'POST', content_type)

        def put(self, url, data={}, content_type='application/json'):
            return self._request(url, data, 'PUT', content_type)

        def delete(self, url, data=None, content_type='application/json'):
            return self._request(url, data, 'DELETE', content_type)

# For Python 3, urllib2 will cause ImportError
except ImportError:
    import urllib.request, urllib.parse, urllib.error

    class Request:
        
        def _request(self, url, data, action, content_type):

            if ((data or isinstance(data, dict)) and
                action not in ('GET', 'DELETE',)):
                data = json.dumps(data)
                # Added encoding for Py3
                data = data.encode('ascii')
                if action == 'PUT':
                    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
                    req = urllib.request.Request(url, data=data)
                    req.add_header('Content-Type', content_type)
                    req.get_method = lambda: 'PUT'
                    conn = opener.open(req)
                else:
                    headers = {'Content-Type': content_type}
                    try:
                        req = urllib.request.Request(url, data, headers)
                        conn = urllib.request.urlopen(req)
                    except TypeError:
                        # This is for the _lights.find bodyless POST.
                        data = urllib.parse.urlencode(data, 1)
                        req = urllib.request.Request(url, data, headers)
                        conn = urllib.request.urlopen(req)
            elif action == 'DELETE':
                opener = urllib.request.build_opener(urllib.request.HTTPHandler)
                req = urllib.request.Request(url)
                req.get_method = lambda: 'DELETE'
                conn = opener.open(req)
            else:
                req = urllib.request.Request(url)
                conn = urllib.request.urlopen(req)
            response = conn.read()
            conn.close()
            try:
                content = json.loads(response)
            except:
                content = response
            # Removed header attr from conn.info() for Py3
            return conn.info(), content

        def get(self, url, data=None, content_type='application/json'):
            return self._request(url, data, 'GET', content_type)

        def post(self, url, data={}, content_type='application/json'):
            return self._request(url, data, 'POST', content_type)

        def put(self, url, data={}, content_type='application/json'):
            return self._request(url, data, 'PUT', content_type)

        def delete(self, url, data=None, content_type='application/json'):
            return self._request(url, data, 'DELETE', content_type)
