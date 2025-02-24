from app import create_app, db
from app.models import City, Town, Category

# Initialize Flask app
app = create_app()

with app.app_context():
    # Define town mappings for each city
    towns_dict = {
        "Kampala": ["Nabweru", "Bwaise", "Ntinda", "Wandegeya", "Makindye", "Kawempe", "Rubaga", "Central", "Kibuye", "Nakasero", "Kololo", "Muyenga", "Bugolobi", "Makerere"],
        "Wakiso": ["Nansana", "Kakiri", "Buloba", "Kyengera", "Mpigi", "Matugga", "Kasangati", "Busukuma"],
        "Gulu": ["Makindye", "Layibi", "Laroo", "Pece", "Bardege", "Bungatira", "Patiko"],
        "Mbarara": ["Katete", "Kakoba", "Nyamitanga", "Ruti", "Biharwe", "Makenke", "Rugazi"],
        "Luweero": ["Kasana", "Bombo", "Wobulenzi", "Zirobwe", "Kamira", "Butuntumula", "Luwero Town"],
        "Masaka": ["Katwe", "Kijjabwemi", "Nyendo", "Kimaanya", "Bukoto"],
        "Apac": ["Atana", "Arocha", "Teboke", "Chegere", "Ibuje", "Akokoro"],
        "Soroti": ["Arapai", "Katine", "Gweri", "Madera", "Opuyo", "Amuria", "Serere"],
        "Nakasongola": ["Kakooge", "Lwampanga", "Kibira", "Zengebe", "Kalungi", "Kalongo"],
    }

    # Fetch all categories
    categories = Category.query.all()

    for category in categories:
        print(f"Processing towns for category: {category.name}...")

        # Get cities under the category
        cities = City.query.filter_by(category_id=category.id).all()

        for city in cities:
            if city.name in towns_dict:
                existing_town_names = {town.name for town in city.towns}  # Prevent duplicates
                
                for town_name in towns_dict[city.name]:
                    if town_name not in existing_town_names:
                        new_town = Town(name=town_name, city=city)
                        db.session.add(new_town)

    # Commit the changes
    db.session.commit()
    print("✅ Successfully assigned identical towns to all cities across all categories!")
