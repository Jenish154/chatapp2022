from chatapp import app, create_database, server_socket

if __name__ == '__main__':
	create_database(app)
	server_socket.run(app, debug = True)