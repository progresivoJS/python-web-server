from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi # common gateway interface

import restaurant_dao

# Handler
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                
            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                id = self.path.split('/')[2]
                restaurant = restaurant_dao.read_restaurant_by_id(id)
                output = "<html><body>"
                output += "<h2>{}</h2>".format(restaurant.name)
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{}/edit'>".format(id)
                output += "<input name='newRestaurantName' type='text' placeholder='{}'>".format(restaurant.name)
                output += "<input type='submit' value='Rename'></form>"
                output += "</body></html>"

                self.wfile.write(output.encode())

                return

            elif self.path.endswith("/restaurants/new"):
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
                    output += "<h3><a href='/restaurants/{}/edit'>Edit</a></h3>".format(restaurant.id)
                    output += "<h3><a href='/restaurants/{}/delete'>Delete</a></h3>".format(restaurant.id)
                output += "<h2><a href='/restaurants/new'>Add new restaurant</a></h2>"
                output += "</body></html>"

                self.wfile.write(output.encode()) # In python 3, parameter of the write have to be byte-like.
                return
        
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

                if ctype == 'multipart/form-data':
                    fileds = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fileds.get('newRestaurantName')

                id = self.path.split('/')[2]
                restaurant_dao.edit_restaurant(id, new_restaurant_name[0].decode())

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            elif self.path.endswith("/restaurants/new"):
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