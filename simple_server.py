from http.server import HTTPServer, BaseHTTPRequestHandler

# html server  work 



html = '''
<h1>hello man</h1>
<button>press me </button>
'''

class SimpleHTTPhandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
        


def run():
    address = ('localhost',4001)
    httpd = HTTPServer(address, SimpleHTTPhandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run()
    
    