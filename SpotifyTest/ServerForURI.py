import http.server
import socketserver

import urllib

from urllib import request

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/RedirectSuccess':
            # serve the redirect_successful.html file
            with open("D:\WorkFiles\LangChainRepo\LangChainProject\RedirectPage.html", 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
        else:
            # serve static files or handle other requests
            super().do_GET()

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()