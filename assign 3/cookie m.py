import socket

HOST, PORT = '', 8080

def create_response(body, cookie=None):
    """Construct a basic HTTP response with optional cookie."""
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    if cookie:
        response += f"Set-Cookie: session_id={cookie}\r\n"
    response += "\r\n"
    response += body
    return response

def parse_cookies(request_headers):
    """Parse cookies from the request headers."""
    cookies = {}
    for header in request_headers:
        if header.lower().startswith("cookie:"):
            cookie_data = header.split(':', 1)[1].strip()
            for pair in cookie_data.split(';'):
                if '=' in pair:
                    key, value = pair.strip().split('=', 1)
                    cookies[key.strip()] = value.strip()
    return cookies

def handle_request(client_socket):
    """Process an incoming client HTTP request."""
    request_data = client_socket.recv(1024).decode('utf-8')
    if not request_data:
        return

    headers = request_data.split('\r\n')
    print("📩 Incoming HTTP request:")
    print(request_data)
    print("────────────────────────")

    cookies = parse_cookies(headers)

    if 'session_id' in cookies:
        user_id = cookies['session_id']
        body = f"<h1>Welcome back, {user_id}!</h1><p>Your session is maintained.</p>"
        response = create_response(body)
    else:
        user_id = "User123"
        body = "<h1>Welcome, new visitor!</h1><p>A cookie has been set for your session.</p>"
        response = create_response(body, cookie=user_id)

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def run_server():
    """Start a simple HTTP server that handles cookies."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"🍪 Cookie server running at http://localhost:{PORT}")
        print("🔄 Waiting for client connections...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"✅ Connected to client: {addr}")
            handle_request(client_socket)

if __name__ == '__main__':
    run_server()
