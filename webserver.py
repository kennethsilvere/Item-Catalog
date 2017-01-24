from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem



engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                try:
                        if self.path.endswith("/delete"):
                                restaurantIDPath = self.path.split("/")[2]
                                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                                if myRestaurantQuery != []:
                                        self.send_response(200)
                                        self.send_header('Content-type', 'text/html')
                                        self.end_headers()
                                        output = ""
                                        output += "<html><body>"
                                        output += "<h1>"
                                        output += "Do you want to delete the restaurant %s ?" % myRestaurantQuery.name
                                        output +="</h1>"
                                        output += '''<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/delete"><br>''' % restaurantIDPath
                                        output += "<input type='submit' value='delete'>"
                                        output += "</form></body></html>"

                                        self.wfile.write(output)


                        if self.path.endswith("/edit"):
                                restaurantIDPath = self.path.split("/")[2]
                                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                                if myRestaurantQuery != []:
                                        self.send_response(200)
                                        self.send_header('Content-type', 'text/html')
                                        self.end_headers()
                                        output = ""
                                        output += "<html><body>"
                                        output += "<h1>"
                                        output += myRestaurantQuery.name
                                        output +="</h1>"
                                        output += '''<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/edit"><br>''' % restaurantIDPath
                                        output += '''<input name="newRestaurantName" type="text" placeholder="%s">''' % myRestaurantQuery.name
                                        output += "<input type='submit' value='Rename'>"
                                        output += "</form></body></html>"

                                        self.wfile.write(output)
                                        
                                        

                        
                        if self.path.endswith("/restaurants/new"):
                                self.send_response(200)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers()
                                output = ""
                                output += "<html><body>"
                                output += '''<form method="POST" enctype="multipart/form-data" action="/restaurants/new"><label>Make new restaurant</label><br>
                                <input name="newRestaurantName" type="text"><br>'''
                                output += '<input type="submit" value="create">'
                                output += '</body></html>'

                                self.wfile.write(output)
                                return
                                         



                        
                        if self.path.endswith("/restaurants"):
                                restaurants = session.query(Restaurant).all()
                                self.send_response(200)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers() 
                                output =""
                                output +="<html><body>"
                                output +='<a href="/restaurants/new">Make new restaurant</a><br><br>' 
                                for restaurant in restaurants:
                                        output += restaurant.name
                                        output += "<br>"
                                        output += '<a href="restaurants/%s/edit">Edit</a><br>' % restaurant.id
                                        output += '<a href="restaurants/%s/delete">Delete</a><br><br>' % restaurant.id
                                        
                                output += "</body></html>"
                                self.wfile.write(output)
                                print output
                                return



                        
                        if self.path.endswith("/hello"):
                                self.send_response(200)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers()
                                output = ""
                                output += "<html><body>"
                                output += "<h1>Hello!</h1>"
                                output += '''<form method='POST' enctype='multipart/form-data' action='http://localhost:8080/'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''

                                output += "</body></html>"
                                self.wfile.write(output)
                                print output
                                return

                        if self.path.endswith("/hola"):
                                
                                self.send_response(200)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers()
                                output = ""
                                output += "<html><body>"
                                output += "<h1>&#161 Hola !</h1>"
                                output += '''<form method='POST' enctype='multipart/form-data' action='http://localhost:8080/'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                                output += "</body></html>"
                                self.wfile.write(output)
                                print output
                                return

                except IOError:
                        self.send_error(404, 'File Not Found: %s' % self.path)


        def do_POST(self):
                try:
                        if self.path.endswith("/delete"):
                                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                                restaurantIDPath = self.path.split("/")[2]
                                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                                if myRestaurantQuery != []:
                                        session.delete(myRestaurantQuery)
                                        session.commit()
                                        self.send_response(301)
                                        self.send_header('Content-type', 'text/html')
                                        self.send_header('Location', '/restaurants')
                                        self.end_headers()
                                        return

                        
                        if self.path.endswith("/edit"):
                                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                                if ctype == 'multipart/form-data':
                                        fields=cgi.parse_multipart(self.rfile, pdict)
                                        messagecontent = fields.get('newRestaurantName')
                                        restaurantIDPath = self.path.split("/")[2]

                                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                                if myRestaurantQuery != []:
                                        myRestaurantQuery.name = messagecontent[0]
                                        session.add(myRestaurantQuery)
                                        session.commit()
                                        self.send_response(301)
                                        self.send_header('Content-type', 'text/html')
                                        self.send_header('Location', '/restaurants')
                                        self.end_headers()
                                        return
                                        




                        
                        if self.path.endswith("/restaurants/new"):
                                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                                if ctype == 'multipart/form-data':
                                        fields=cgi.parse_multipart(self.rfile, pdict)
                                        messagecontent = fields.get('newRestaurantName')

                                newRestaurant = Restaurant(name = messagecontent[0])
                                session.add(newRestaurant)
                                session.commit()

                                self.send_response(301)
                                self.send_header('Content-type', 'text/html')
                                self.send_header('Location', '/restaurants')
                                self.end_headers()
                                return
                                



                        
                        self.send_response(301)
                        self.end_headers()

                        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                        if ctype == 'multipart/form-data':
                                fields=cgi.parse_multipart(self.rfile, pdict)
                                messagecontent = fields.get('message')

                                output = ""

                                output +=  "<html><body>"
                                output += " <h2> Okay, how about this: </h2>"

                                output += "<h1> %s </h1>" % messagecontent[0]

                                output += '''<form method='POST' enctype='multipart/form-data' action='http://localhost:8080/'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
			

                                output += "</html></body>"

                                self.wfile.write(output)
                                print output

                except:
                        pass


def main():
        try:
                port = 8080
                server = HTTPServer(('', port), webServerHandler)
                print "Web Server running on port %s"  % port
                server.serve_forever()
                
        except KeyboardInterrupt:
                print " ^C entered, stopping web server...."
                server.socket.close()

if __name__ == '__main__':
	main()
