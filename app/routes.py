from flask import Blueprint, render_template, request, jsonify
from . import db
from .models import Advisor

main = Blueprint('main', __name__)

@main.route('/')
def home():
    advisors = Advisor.query.all()
    return render_template('index.html', advisors=advisors)

@main.route('/add_advisor', methods=['POST'])
def add_advisor():
    data = request.get_json()
    new_advisor = Advisor(name=data['name'], profession=data['profession'], reviews=data.get('reviews', ''))
    db.session.add(new_advisor)
    db.session.commit()
    return jsonify({'message': 'Advisor added successfully!'})

# Add this route for the register page
@main.route('/register')
def register():
    return render_template('register.html')

# Add this route for the login page
@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@main.route('/category/<category>/<city>')
def category_city(category, city):
    # You can fetch data from the database for the specific category and city here
    return render_template('category_city.html', category=category, city=city)


