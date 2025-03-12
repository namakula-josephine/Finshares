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
    
@main.route('/town/<town_name>')
def town_page(town_name):
    # Fetch the town
    town = Town.query.filter_by(name=town_name).first()
    if not town:
        return "Town not found", 404

    # Fetch the city and category
    city = City.query.get(town.city_id)
    category = Category.query.get(city.category_id)

    # Fetch all advisors in this town's city
    advisors = Advisor.query.filter_by(city_id=city.id)

    # Apply filters based on user selection
    service = request.args.get('service')
    savings = request.args.get('savings')
    distance = request.args.get('distance')

    if service:
        advisors = advisors.filter(Advisor.services.contains(service))
    if savings:
        advisors = advisors.filter(Advisor.savings_level.contains(savings))
    if distance:
        advisors = advisors.filter(Advisor.distance_level.contains(distance))

    return render_template('town.html', town=town, city=city, category=category, advisors=advisors)
    
@main.route('/static/images/<filename>')
def static_images(filename):
    return send_from_directory(os.path.join(main.root_path, 'static', 'images'), filename)
