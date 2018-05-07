from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi # common gateway interface

import restaurant_dao

# Handler
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = "<html><body>"
                output += "<h2>What is the name of new restaurant?</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output.encode())
                return

            elif self.path.endswith("/restaurants"):
                self.send_response(200) # success code of get request
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = restaurant_dao.read_all_restaurants()

                output = "<html><body>"
                for restaurant in restaurants:
                    output += "<h2>{}</h2>".format(restaurant.name)
                    output += "<h3><a href=''>Edit</a></h3>"
                    output += "<h3><a href=''>Delete</a></h3>"
                output += "<h2><a href='/restaurants/new'>Add new restaurant</a></h2>"
                output += "</body></html>"

                self.wfile.write(output.encode()) # In python 3, parameter of the write have to be byte-like.
                return
        
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('newRestaurantName')

                restaurant_dao.add_new_restaurant(new_restaurant_name[0].decode())
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

        except:
            pass

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