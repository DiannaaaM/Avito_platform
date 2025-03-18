import os
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
PORT = 8000

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

if __name__ == "__main__":
    webServer = HTTPServer((hostName, PORT), MyServer)
    print(f"Server started at http://{hostName}:{PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")