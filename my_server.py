#!/usr/bin/env python
"""
Very simple HTTP server in python (Updated for Python 3.7)

Usage:

    ./dummy-web-server.py -h
    ./dummy-web-server.py -l localhost -p 8000

Send a GET request:

    curl http://localhost:8000

Send a HEAD request:

    curl -I http://localhost:8000

Send a POST request:

    curl -d "foo=bar&bin=baz" http://localhost:8000

"""
import argparse
from urllib.parse import urlparse, quote_plus
from http.server import HTTPServer, BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):
    
    ROOT = "nonprod_base_bucket"

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def._wrap_response(self, message):
        content = f"{message}"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        file_path = self._handle_url()
        self.wfile.write(self._wrap_response(file_path))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._wrap_response("POST!"))
        
    def _handle_url(self):
        # content_len = int(self.headers.get('Content-Length'))
        url = urlparse(self.path)
        return self._convert_url_to_file_path(url.path,
                                              quote_plus(url.query) if url.query != "" else "no_query")

    def _convert_url_to_file_path(self, path, filename, extension="txt"):
        return f"{self.ROOT}{path}/{filename}.{extension}"

    def _convert_url_to_header_record(self, path):
        return f"{self.ROOT}{path}/header"
        

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
