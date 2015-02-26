import httplib
import pudb
pudb.set_trace()

USER_AGENT = "httplib-example-1.py"

class Error:
    # Indicates an HTTP Error
    def __init__(self, url, errcode, errmsg, headers):
        self.url = url
        self.errcode = errcode
        self.headers = headers

    def __repr__(self):
        return (
                "<Error for %s: %s %s>" %
                (self.url, self.errcode, self.errmsg)
                )

class Server:
    def __init__(self, host):
        self.host = host
    def fetch(self, path):
        http = httplib.HTTP(self.host)

        # Write header
        http.putheader("GET",path)
        http.putheader("User-Agent", USER_AGENT)
        http.putheader("Host", self.host)
        http.putheader("Accept", "*/*")
        http.endheaders()

        # get response
        errcode, errmsg, headers = http.getreply()

        if errcode != 200:
            raise Error(errcode, errmsg, headers)

        f = http.getfile()
        return f.read()

if __name__ == '__main__':
    server = Server("www.pythonware.com")
    print server.fetch("/index.htm")
