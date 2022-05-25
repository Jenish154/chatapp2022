from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required
from chatapp import db, chat_bcrypt, server_socket
from .forms import RegistrationForm, LoginForm
from .models import User, Message

user = Blueprint('user', __name__)

@server_socket.on('message')
def recieve_message(data):
	print(f'[NEW MESSAGE]: {data}')
	sender_acc = User.query.filter_by(username = data['sender']).first()
	reciever_acc = User.query.filter_by(username = data['reciever']).first()
	new_msg = Message(content = data['data'], sender = sender_acc.id, reciever = reciever_acc.id)
	db.session.add(new_msg)
	db.session.commit()

@user.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		print(f'email: {form.username.data}')
		check_username = User.query.filter_by(username = form.username.data).first()
		check_email = User.query.filter_by(email = form.email.data).first()
		if check_email or check_username:
			print('values', type(check_email), type(check_username))
			flash('Username or email already in use. Try again', 'warning')
		else:
			hash_pw = chat_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			new_user = User(username = form.username.data, email = form.email.data, password = hash_pw)
			db.session.add(new_user)
			db.session.commit()
			flash(f'Account created succesfully for {form.username.data}', 'success')
			return redirect(url_for('user.login'))
	return render_template('register.html', form = form)

@user.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		password = form.password.data
		cur_user = User.query.filter_by(email = form.email.data).first()
		if not cur_user:
			flash('No such account exists. Try again!', 'warning')
		else:
			if chat_bcrypt.check_password_hash(cur_user.password, password):
				flash('Logged in successfully!', 'success')
				login_user(cur_user)
				return redirect(url_for('main.home'))
			else:
				flash('Incorrect password. Try again!', 'error')
	return render_template('login.html', form = form)
	
@user.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.landing'))
	
@user.route('/profile/<name>')
@login_required
def profile(name: str):
	if not name:
		abort(404)
	else:
		profile_user = User.query.filter_by(username = name).first()
		if not profile_user:
			abort(404)
		else:
			return render_template('profile.html', user = profile_user)

@user.route('/message/<reciever>')
@login_required
def message(reciever):
	if not reciever:
		abort(404)
	else:
		recv_acc = User.query.filter_by(username = reciever).first()
		if not recv_acc:
			abort(404)
		print('here'+ ("\n"*10))
		print(current_user)
		ex_messages = Message.query.filter_by(sender = current_user.id).all()
		new_msg = []
		for i in ex_messages:
			if i.reciever == recv_acc.id:
				new_msg.append(i)
		return render_template('message.html', reciever = recv_acc, messages = new_msg)