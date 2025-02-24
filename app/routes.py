from flask import Blueprint, render_template, request, jsonify
import urllib
from . import db
from flask import send_from_directory
import os
from .models import Advisor, Category, City, Town  # Import models
from urllib.parse import unquote 

main = Blueprint('main', __name__)

@main.route('/')
def home():
    advisors = Advisor.query.all()  # Ensure the table exists
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


def home():
    """ ✅ Render the homepage with all categories and cities dynamically """
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@main.route('/category/<category>/<city>')
def category_city(category, city):
    """ ✅ Fetch full category name, city, and towns """
    
    # Decode URL-encoded category name (handles spaces and & symbols)
    category_decoded = urllib.parse.unquote(category)
    city_decoded = urllib.parse.unquote(city)

    # Fetch category from the database
    category_obj = Category.query.filter_by(name=category_decoded).first()
    if not category_obj:
        return f"❌ Category '{category_decoded}' not found", 404

    # Fetch the city within that category
    city_obj = City.query.filter_by(name=city_decoded, category_id=category_obj.id).first()
    if not city_obj:
        return f"❌ City '{city_decoded}' not found in category '{category_decoded}'", 404

    # Fetch towns in this city
    towns = Town.query.filter_by(city_id=city_obj.id).all()

    # ✅ Debugging: Print values to see what's passed
    print(f"✅ Category: {category_obj.name}")  
    print(f"✅ City: {city_obj.name}")  
    print(f"✅ Towns: {[town.name for town in towns]}")  

    return render_template(
        'category_city.html', 
        category=category_obj.name,  # ✅ Pass full category name
        city=city_obj,  # ✅ Ensure full city name is passed
        towns=towns
    )
    
@main.route('/static/images/<filename>')
def static_images(filename):
    return send_from_directory(os.path.join(main.root_path, 'static', 'images'), filename)
