from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse
import importlib.resources

# Read a data file from the package
with importlib.resources.open_text("src", "index.html") as data_file:
    html_content = data_file.read()
    # print(f"Data file contents: {data}")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # content of the html file from the web_application/index.h
        parsed_path = urlparse(self.path)
        print(parsed_path.path)

        file_content = html_content.encode()
        # if parsed file path is not empty
        if parsed_path.path != "/" and parsed_path.path != "":
            file_path = parsed_path.path[1:]
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    file_content = file.read()
            else:
                self.send_response(404)
                self.end_headers()
                return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(file_content)


def runWebServer(
    server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000
):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()
