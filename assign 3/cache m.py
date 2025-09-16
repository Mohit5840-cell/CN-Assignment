import http.server
import socketserver
import os
import hashlib
from datetime import datetime
from email.utils import formatdate

PORT = 8000
FILE_TO_SERVE = "index.html"


def generate_etag(file_path):
    """Generate an MD5-based ETag from the file contents."""
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    return f'"{file_hash}"'


def get_last_modified(file_path):
    """Get the file's last modification time in HTTP date format."""
    mtime = os.path.getmtime(file_path)
    return formatdate(timeval=mtime, usegmt=True)


class CachingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Force all requests to serve the specified file
        if self.path == '/':
            self.path = FILE_TO_SERVE

        file_path = self.translate_path(self.path)

        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return

        etag = generate_etag(file_path)
        last_modified = get_last_modified(file_path)

        # Retrieve client cache headers
        client_etag = self.headers.get("If-None-Match")
        client_last_modified = self.headers.get("If-Modified-Since")

        # Check for strong validator match (ETag)
        if client_etag == etag:
            self.send_response(304)
            self.end_headers()
            return

        # Check for weak validator match (Last-Modified)
        if client_last_modified == last_modified:
            self.send_response(304)
            self.end_headers()
            return

        # If no match, respond with file and caching headers
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_modified)
        self.end_headers()

        with open(file_path, "rb") as f:
            self.wfile.write(f.read())


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CachingHTTPRequestHandler) as httpd:
        print(f"🚀 Server is running at http://localhost:{PORT}")
        httpd.serve_forever()
