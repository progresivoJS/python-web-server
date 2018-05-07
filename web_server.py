from http.server import BaseHTTPRequestHandler, HTTPServer

# Handler
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello") or self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                if self.path.endswith("/hello"):
                    output = ""
                    output += "<html><body>Hello!</body></html>"
                elif self.path.endswith("/hola"):
                    output = ""
                    output += "<html><body>&#161Hola <a href = '/hello'>Back to Hello</a></body></html>"
                self.wfile.write(output.encode()) # In python 3, parameter of the write have to be byte-like.
                print(output)
                return
        
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

# main
def main():
    try:
        port = 8080

        # server address is expressed as tuple(ip, port).
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()

    # When the user holds Ctrl + C on the keyboard.
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()