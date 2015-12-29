from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()	
				output = ""
				output += "<html><body>"
				output += "<h1>&#161 Hola !</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new'>Click here to enter a new restaurant</a>"
				output += "</br>"
				output += "</br>"
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					output += restaurant.name
					output += "</br>"
					output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
					output += "</br>"
					output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
					output += "</br>"
					output += "</br>"
					output += "</html></body>"
				self.wfile.write(output)
				print output
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='restaurants/new'>"
				output += '''<input name='message' type='text' placeholder='New Restaurant Name'>
					<input type="submit" value="Create">'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
			restaurants = session.query(Restaurant).all()
			for restaurant in restaurants:
				if self.path.endswith("/restaurants/%s/edit" % restaurant.id):
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>%s</h1>" % restaurant.name
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant.id
					output +='''<input name='message' type='text' placeholder='Updated Restaurant Name' >
						<input type='submit' value='Update'></form>'''
					output += "</body></html>"
					self.wfile.write(output)
					print output
				if self.path.endswith("/restaurants/%s/delete" % restaurant.id):
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
					output += "<form method='Post' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant.id
					output += "<input type='submit' value='Delete'></form>"
					output += "</body></html>"
					self.wfile.write(output)
					print output
			
		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			
			ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
			if self.path.endswith("/hello"):
				output = ""
				output += "<html><body>"
				output += " <h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
			if self.path.endswith("/restaurants/new"):
				output = ""
				newrest = Restaurant(name= messagecontent[0])
				session.add(newrest)
				session.commit()
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				print output
			restaurants = session.query(Restaurant).all()
			for restaurant in restaurants:
				if self.path.endswith("/restaurants/%s/edit" % restaurant.id):
					output = ""
					restaurant.name = "%s" % messagecontent[0]
					session.add(restaurant)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
					print output
				if self.path.endswith("/restaurants/%s/delete" % restaurant.id):
					output = ""
					#deleterest = session.query(Restaurant).filter_by(id=restaurant.id).one()
					session.delete(restaurant)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
			
		except:
			pass


def main():
	try:
		port = 8000
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()