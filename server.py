
from http.server import HTTPServer, BaseHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader
import json
import socket
import logging
import pathlib
from threading import Thread
import urllib
from datetime import datetime

env = Environment(loader=FileSystemLoader('templates'))
BASE_DIR = pathlib.Path('.')
BUFFER_SIZE = 1024
PORT_HTTP = 3000
SOCKET_PORT = 4000
SOCKET_HOST = '127.0.0.1'

def send_data_to_socket(data):
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_socket.sendto(data, (SOCKET_HOST, SOCKET_PORT))
    c_socket.close()


class Best_Server(BaseHTTPRequestHandler):

    def do_POST(self):
        lenght = self.headers.get('Content-Length')
        data = self.rfile.read(int(lenght))
        send_data_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/form')
        self.end_headers()

    def do_GET(self):
        round = urllib.parse.urlparse(self.path)
        print(round.path)
        match round.path:
            case '/':
                self.render_template('home.html')
            case '/about':
                self.render_template('about.html')
            case '/form':
                self.render_template('form.html')
            case _:
                file = BASE_DIR.joinpath(round.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.render_template('404.html')
                self.render_template('404.html')

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def render_template(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        template = env.get_template(filename)
        with open ('storage/blog.json',  'rb') as fd:
            blogs = json.load(fd)
        html = template.render(title=filename.split('.')[0], blogs=blogs)
        self.wfile.write(html.encode())

def save_data_from_http_server(data):
    decode_data = data.decode()    
    try:
        all_data = {key:value for key, value in [el.split('=') \
                         for el in decode_data.split('&')]}
        
        with open('data/data.json') as json_file:
            data = json.load(json_file)
        data[str(datetime.now())] = all_data

        with open('data/data.json','w', encoding='utf-8') as fd:            
            json.dump(data, fd,  ensure_ascii=False, indent=4)

    except OSError as err:
        logging.debug(f'ERRORORO {decode_data} error , {err}')    
    except ValueError as err:
        logging.debug(f'for data {decode_data} error , {err}')

    

def run_socket_server(host, port):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_socket.bind((host, port))

    try:
        while True:
            # TCP дает нам именно байты, поэтому их надо декодировать
            msg,  address = s_socket.recvfrom(BUFFER_SIZE)
            save_data_from_http_server(msg)
    except KeyboardInterrupt:
        logging.info('socket server stopped')
    finally:    
        s_socket.close()

def run_http_server():
    address = ('0.0.0.0',PORT_HTTP)
    httpd = HTTPServer(address, Best_Server)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info('socket server stopped "run"')
        httpd.server_close()
    finally:
        httpd.server_close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s' )
    th_server = Thread(target=run_http_server)
    th_server.start()

    th_socket = Thread(target=run_socket_server, args=(SOCKET_HOST, SOCKET_PORT,))
    th_socket.start()


    
    