from flask import Blueprint, render_template, request, jsonify
from . import db
from flask import send_from_directory
import os
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

@main.route('/register')
def register():
    return render_template('register.html')

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


@main.route('/static/images/<filename>')
def static_images(filename):
    return send_from_directory(os.path.join(main.root_path, 'static', 'images'), filename)