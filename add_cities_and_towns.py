from app import db, create_app
from app.models import Category, City, Town

# Create the app context
app = create_app()
with app.app_context():
    # Define categories and their cities
    category_data = {
        "Solicitors": [
            "Kampala", "Wakiso", "Gulu", "Soroti", "Apac", "Luweero", "Masaka", "Mbarara"
        ],
        "Accountants": [
            "Kampala", "Wakiso", "Gulu", "Soroti", "Apac", "Luweero", "Masaka", "Mbarara"
        ]
    }

    # Ensure categories exist
    for category_name, cities in category_data.items():
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
            print(f"✅ Created category: {category_name}")

        # Add cities under the category
        for city_name in cities:
            city = City.query.filter_by(name=city_name, category=category).first()
            if not city:
                new_city = City(name=city_name, category=category)
                db.session.add(new_city)
                print(f"✅ Added city: {city_name} under {category_name}")

    db.session.commit()

    # Define towns for each city
    towns_data = {
        "Kampala": ["Nakasero", "Kololo", "Muyenga", "Bugolobi", "Makerere"],
        "Wakiso": ["Nansana", "Kakiri", "Buloba", "Kyengera", "Matugga"],
        "Gulu": ["Layibi", "Laroo", "Pece", "Bardege", "Patiko"],
        "Soroti": ["Arapai", "Katine", "Gweri", "Madera", "Opuyo"],
        "Apac": ["Atana", "Arocha", "Teboke", "Chegere", "Ibuje"],
        "Luweero": ["Kasana", "Bombo", "Wobulenzi", "Zirobwe", "Butuntumula"],
        "Masaka": ["Katwe", "Kijjabwemi", "Nyendo", "Bukoto", "Kimaanya"],
        "Mbarara": ["Kakoba", "Nyamitanga", "Ruti", "Biharwe", "Makenke"]
    }

    for city_name, town_list in towns_data.items():
        city = City.query.filter_by(name=city_name).first()
        if city:
            for town_name in town_list:
                existing_town = Town.query.filter_by(name=town_name, city=city).first()
                if not existing_town:
                    new_town = Town(name=town_name, city=city)
                    db.session.add(new_town)
                    print(f"✅ Added town: {town_name} in {city_name}")

    # Commit all changes
    db.session.commit()
    print("🎉 All cities & towns added successfully!")
