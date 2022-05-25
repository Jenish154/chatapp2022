import datetime
from chatapp import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(120), unique = True, nullable = False)
	contacts = db.relationship('Contact', backref = 'user', lazy = True)
	profile = db.Column(db.String(120), default= 'default.png')        #profile pic's filename
	
	def __repr__(self):
		return f'User:<Username: {self.username} Email: {self.email}>'

class Message(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	sender = db.Column(db.Integer, nullable = False)           #sender's id
	reciever = db.Column(db.Integer, nullable = False)         #reciever's id
	content = db.Column(db.String(2000), nullable = False)
	date = db.Column(db.DateTime(), default = datetime.datetime.now())
	
	def __repr__(self):
		print(f'Message<from: {self.sender} to: {self.reciever} timestamp: {self.date}>')
	
class Contact(db.Model):
	id = db.Column(db.Integer, primary_key = True)	                                #contacts id
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)     #user's id
	
	
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))