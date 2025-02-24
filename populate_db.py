from app import db, create_app
from app.models import Category, City

# Create the app context
app = create_app()
with app.app_context():
    # Check if the category exists
    category = Category.query.filter_by(name="Financial & Mortgage Advisers").first()
    
    if not category:
        # Create and add the category if it doesn't exist
        category = Category(name="Financial & Mortgage Advisers")
        db.session.add(category)
        db.session.commit()
        print("✅ Category 'Financial & Mortgage Advisers' added successfully!")

    # List of new cities to add
    cities_to_add = [
        "Luweero",
        "Masaka",
        "Apac",
        "Soroti",
        "Nakasongola",
        "Gulu",
        "Mbarara"
    ]

    # Add cities only if they don't already exist
    for city_name in cities_to_add:
        existing_city = City.query.filter_by(name=city_name, category_id=category.id).first()
        if not existing_city:
            new_city = City(name=city_name, category=category)
            db.session.add(new_city)
            print(f"✅ Added city: {city_name}")

    # Commit changes
    db.session.commit()
    print("🎉 Database populated successfully!")
