from flask import Blueprint, render_template, url_for, request, redirect, abort
from flask_login import login_required, current_user
from chatapp.users.models import User

main = Blueprint('main', __name__)

dummy_contacts = ['john', 'doe', 'jerry', 'mary']

@main.route('/')
def landing():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	return render_template('landing.html')

@main.route('/home')
@login_required
def home():
	return render_template('home.html', contacts = dummy_contacts)
	
@main.route('/search')
@login_required
def search():
	query = request.args.get('search_query')
	data =  User.query.filter(User.username.startswith(query)).all()
	if data:
		return render_template('search_result.html', data = data)
	else:
		abort(404)
	