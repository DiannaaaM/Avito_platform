from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple, Any
import os

hostName = "localhost"
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/main.html'

        try:
            file_path = os.path.join(os.getcwd(), self.path[1:])
            with open(file_path, 'rb') as file:
                content = file.read()
            self.send_response(200)
            if self.path.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif self.path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f'File Not Found: {self.path}')


def create_handler(*args: Tuple[Any, ...]) -> BaseHTTPRequestHandler:
    return MyServer(*args)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), create_handler)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")