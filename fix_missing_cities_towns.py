from app import create_app, db
from app.models import Category, City, Town

# Initialize Flask app
app = create_app()

with app.app_context():
    # Define categories
    categories = {
        "Financial & Mortgage Advisers": None,
        "Solicitors": None,
        "Accountants": None
    }

    # Fetch categories from the database
    for cat_name in categories.keys():
        category = Category.query.filter_by(name=cat_name).first()
        if category:
            categories[cat_name] = category
            print(f"✅ Found Category: {cat_name}")
        else:
            print(f"❌ Category '{cat_name}' NOT found!")

    # Define cities that should exist in all categories
    city_names = ["Kampala", "Wakiso", "Gulu", "Mbarara", "Luweero", "Masaka", "Apac", "Soroti", "Nakasongola"]

    for cat_name, category in categories.items():
        if not category:
            continue  # Skip if category was not found

        for city_name in city_names:
            # Check if the city already exists in this category
            city = City.query.filter_by(name=city_name, category_id=category.id).first()
            if not city:
                city = City(name=city_name, category=category)
                db.session.add(city)
                print(f"✅ Added missing city '{city_name}' to category '{cat_name}'")
    
    # Commit city additions
    db.session.commit()

    # Define towns for each city
    towns_dict = {
        "Kampala": ["Nabweru", "Bwaise", "Ntinda", "Wandegeya", "Makindye", "Kawempe", "Rubaga", "Central", "Kibuye", "Nakasero", "Kololo", "Muyenga", "Bugolobi", "Makerere"],
        "Wakiso": ["Nansana", "Kakiri", "Buloba", "Kyengera", "Mpigi", "Matugga", "Kasangati", "Busukuma"],
        "Gulu": ["Layibi", "Laroo", "Pece", "Bardege", "Bungatira", "Patiko"],
        "Mbarara": ["Katete", "Kakoba", "Nyamitanga", "Ruti", "Biharwe", "Makenke", "Rugazi"],
        "Luweero": ["Kasana", "Bombo", "Wobulenzi", "Zirobwe", "Kamira", "Butuntumula", "Luwero Town"],
        "Masaka": ["Katwe", "Kijjabwemi", "Nyendo", "Kimaanya", "Bukoto"],
        "Apac": ["Atana", "Arocha", "Teboke", "Chegere", "Ibuje", "Akokoro"],
        "Soroti": ["Arapai", "Katine", "Gweri", "Madera", "Opuyo", "Amuria", "Serere"],
        "Nakasongola": ["Kakooge", "Lwampanga", "Kibira", "Zengebe", "Kalungi", "Kalongo"],
    }

    # Ensure all towns exist under the correct cities in all categories
    for category in categories.values():
        if not category:
            continue  # Skip missing categories
        
        for city in City.query.filter_by(category_id=category.id).all():
            if city.name in towns_dict:
                existing_town_names = {town.name for town in city.towns}  # Prevent duplicates
                
                for town_name in towns_dict[city.name]:
                    if town_name not in existing_town_names:
                        new_town = Town(name=town_name, city=city)
                        db.session.add(new_town)
                        print(f"✅ Added town '{town_name}' to city '{city.name}' in category '{category.name}'")

    # Commit town additions
    db.session.commit()

    print("🎉 All missing cities & towns have been added successfully!")
