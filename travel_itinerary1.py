
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

# API Keys
OPENWEATHER_API_KEY = "8fc7ca2e2fd43e83d0f5f840922ab555"
SPOONACULAR_API_KEY = "91d3bf9798ee471d8f1713142f2817d5"
GEOAPIFY_API_KEY = "74ea38e3e82649ab8148339aab1c070a"

# Famous destinations database
FAMOUS_CITIES = {
    # Global Cities
    "Paris": {
        "landmarks": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Champs-Élysées", "Montmartre"],
        "foods": ["Croissant", "Baguette", "Escargot", "Boeuf Bourguignon", "Macarons"]
    },
    "New York": {
        "landmarks": ["Statue of Liberty", "Times Square", "Central Park", "Empire State Building", "Broadway"],
        "foods": ["New York Pizza", "Bagel with Lox", "Cheesecake", "Pastrami Sandwich", "Hot Dog"]
    },
    "Tokyo": {
        "landmarks": ["Shibuya Crossing", "Tokyo Tower", "Senso-ji Temple", "Meiji Shrine", "Akihabara"],
        "foods": ["Sushi", "Ramen", "Tempura", "Okonomiyaki", "Takoyaki"]
    },
    # Indian Cities
    "Delhi": {
        "landmarks": ["Red Fort", "India Gate", "Qutub Minar", "Lotus Temple", "Chandni Chowk"],
        "foods": ["Butter Chicken", "Chole Bhature", "Paratha", "Kebabs", "Jalebi"]
    },
    "Mumbai": {
        "landmarks": ["Gateway of India", "Marine Drive", "Elephanta Caves", "Chhatrapati Shivaji Terminus", "Juhu Beach"],
        "foods": ["Vada Pav", "Pav Bhaji", "Bombay Sandwich", "Seafood", "Misal Pav"]
    },
    "Bangalore": {
        "landmarks": ["Bangalore Palace", "Lalbagh Botanical Garden", "Cubbon Park", "Vidhana Soudha", "ISKCON Temple"],
        "foods": ["Masala Dosa", "Bisi Bele Bath", "Ragi Mudde", "Mysore Pak", "Filter Coffee"]
    },
    # Add more cities as needed
}

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if 'main' in response:
        return {
            "temperature": response["main"].get("temp", "N/A"),
            "conditions": response["weather"][0].get("description", "N/A") if response.get("weather") else "N/A",
            "humidity": response["main"].get("humidity", "N/A")
        }
    return {"error": "Weather data not available"}

def get_wikipedia_info(city):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city}"
    response = requests.get(url).json()
    return {
        "description": response.get("extract", "No description available"),
        "image": response.get("thumbnail", {}).get("source", "") if response.get("thumbnail") else ""
    }

def get_restaurants(city, budget="Standard"):
    # First check if we have famous local foods for this city
    local_foods = FAMOUS_CITIES.get(city, {}).get("foods", [])

    url = f"https://api.spoonacular.com/food/restaurants/search?query={city}&apiKey={SPOONACULAR_API_KEY}"
    try:
        response = requests.get(url).json()
        restaurants = response.get("restaurants", [])

        # Enhance restaurant data with local food specialties
        for restaurant in restaurants:
            if local_foods:
                restaurant["specialty"] = random.choice(local_foods)

        # Filter by budget
        if budget == "Economy":
            restaurants = [r for r in restaurants if r.get("price_range", "$$$$") in ("$", "$$")]
        elif budget == "Luxury":
            restaurants = [r for r in restaurants if r.get("price_range", "$") in ("$$$", "$$$$")]

        return restaurants[:10]
    except:
        # Fallback to local food specialties if API fails
        return [{"name": f"Local {food} Spot", "specialty": food} for food in local_foods[:5]]

def get_places(city, interests=None):
    if interests is None:
        interests = []

    # First check if we have famous landmarks for this city
    landmarks = FAMOUS_CITIES.get(city, {}).get("landmarks", [])

    categories = []
    if "Adventure" in interests:
        categories.extend(["adventure", "sport"])
    if "Culture" in interests:
        categories.extend(["cultural", "historic", "religion"])
    if "Nature" in interests:
        categories.extend(["natural", "national_park"])
    if "Shopping" in interests:
        categories.append("commercial")
    if not categories:
        categories = ["tourism"]

    all_places = []
    for category in set(categories):
        url = f"https://api.geoapify.com/v2/places?categories={category}&filter=place:{city}&limit=20&apiKey={GEOAPIFY_API_KEY}"
        try:
            response = requests.get(url).json()
            all_places.extend(response.get("features", []))
        except:
            continue

    # Add famous landmarks first
    for landmark in landmarks:
        all_places.insert(0, {
            "properties": {
                "name": landmark,
                "categories": {"name": "Famous Landmark"},
                "address_line2": city
            }
        })

    # Remove duplicates
    unique_places = []
    seen_names = set()
    for place in all_places:
        name = place.get("properties", {}).get("name")
        if name and name not in seen_names:
            unique_places.append(place)
            seen_names.add(name)

    return unique_places[:15]

def generate_daily_activities(day, city, attractions, restaurants, interests):
    landmarks = FAMOUS_CITIES.get(city, {}).get("landmarks", [])
    foods = FAMOUS_CITIES.get(city, {}).get("foods", [])

    # Morning activities
    if landmarks:
        morning = f"Visit {random.choice(landmarks)}"
    elif "Adventure" in interests:
        morning = random.choice([
            "Hiking at a scenic trail",
            "Water sports at a local spot",
            "Cycling tour around the city"
        ])
    else:
        morning = random.choice([
            "Explore the city center",
            "Walking tour of main sights",
            "Visit local markets"
        ])

    # Afternoon activities
    if len(attractions) > 1:
        attraction_names = [a.get("properties", {}).get("name") for a in attractions if a.get("properties", {}).get("name")]
        if attraction_names:
            afternoon = f"Explore {random.choice(attraction_names)}"
        else:
            afternoon = random.choice([
                "Visit a museum or gallery",
                "Discover hidden local gems",
                "Relax at a park or garden"
            ])
    else:
        afternoon = random.choice([
            "Visit a museum or gallery",
            "Discover hidden local gems",
            "Relax at a park or garden"
        ])

    # Evening activities
    evening_options = []
    if "Food" in interests and foods:
        evening_options.append(f"Try famous local {random.choice(foods)}")
    evening_options.extend([
        "Enjoy a local performance or show",
        "Relax at a rooftop bar with city views",
        "Take a sunset cruise or walk"
    ])
    evening = random.choice(evening_options)

    # Lunch recommendation
    lunch = "Try a popular local dish"
    if restaurants:
        restaurant = random.choice(restaurants)
        specialty = restaurant.get("specialty")
        if specialty:
            lunch = f"Lunch at {restaurant.get('name', 'a local restaurant')} - try their {specialty}"
        else:
            lunch = f"Lunch at {restaurant.get('name', 'a local restaurant')}"

    return {
        "day": day,
        "morning": morning,
        "lunch": lunch,
        "afternoon": afternoon,
        "evening": evening
    }

@app.route("/generate_itinerary", methods=["POST"])
def generate_itinerary():
    data = request.json
    city = data.get("city")
    days = data.get("days", 3)
    budget = data.get("budget", "Standard")
    interests = data.get("interests", [])

    if not city:
        return jsonify({"error": "City is required"}), 400

    weather = get_weather(city)
    description = get_wikipedia_info(city)
    restaurants = get_restaurants(city, budget)
    attractions = get_places(city, interests)

    itinerary = []
    for day in range(1, days + 1):
        itinerary.append(generate_daily_activities(day, city, attractions, restaurants, interests))

    response = {
        "weather": weather,
        "description": description.get("description", ""),
        "image": description.get("image", ""),
        "restaurants": restaurants,
        "attractions": [attraction.get("properties", {}) for attraction in attractions],
        "itinerary": itinerary,
        "local_specialties": FAMOUS_CITIES.get(city, {}).get("foods", []),
        "famous_landmarks": FAMOUS_CITIES.get(city, {}).get("landmarks", [])
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
