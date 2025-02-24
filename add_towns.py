from app import db, create_app
from app.models import City, Town

# Create the app context
app = create_app()
with app.app_context():
    # Define towns for each city
    towns_data = {
        "Kampala": ["Nabweru", "Bwaise", "Ntinda", "Wandegeya", "Makindye", "Kawempe", "Rubaga", "Central", "Kibuye"],
        "Wakiso": ["Nansana", "Kakiri", "Buloba", "Kyengera", "Mpigi", "Matugga", "Kasangati", "Busukuma"],
        "Luweero": ["Kasana", "Bombo", "Wobulenzi", "Zirobwe", "Kamira", "Butuntumula", "Luwero Town"],
        "Masaka": ["Katwe", "Kijjabwemi", "Nyendo", "Kimaanya", "Kijjabwemi", "Bukoto"],
        "Apac": ["Atana", "Arocha", "Teboke", "Chegere", "Ibuje", "Akokoro"],
        "Soroti": ["Arapai", "Katine", "Gweri", "Madera", "Opuyo", "Amuria","Serere"],
        "Nakasongola": ["Kakooge", "Lwampanga", "Kibira", "Zengebe", "Kalungi", "Kalongo"],
        "Gulu": ["Layibi", "Laroo", "Pece", "Bardege", "Bungatira", "Patiko"],
        "Mbarara": ["Kakoba", "Nyamitanga", "Ruti", "Biharwe", "Makenke", "Rugazi"]
    }

    for city_name, town_list in towns_data.items():
        city = City.query.filter_by(name=city_name).first()
        
        if city:
            for town_name in town_list:
                # Check if town already exists
                existing_town = Town.query.filter_by(name=town_name, city_id=city.id).first()
                if not existing_town:
                    new_town = Town(name=town_name, city=city)
                    db.session.add(new_town)
                    print(f"✅ Added town: {town_name} in {city_name}")
    
    # Commit all changes
    db.session.commit()
    print("🎉 All towns added successfully!")
