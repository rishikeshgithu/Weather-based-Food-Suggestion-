import requests

# ======== CONFIGURATION ========
WEATHER_API_KEY = "9f3ff2a5df2e424ea8110613250706"
cities = ["Chennai", "Delhi", "Kolkata"]
meals = ["Breakfast", "Lunch", "Dinner"]


# ======== UTILITIES ========
def safe_get(d, *keys):
    for key in keys:
        d = d.get(key, {})
    return d if d else "Unknown"


# ======== STEP 1: WEATHER LOGIC ========
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    try:
        res = requests.get(url).json()
        condition = safe_get(res, "current", "condition", "text")
        temp_c = safe_get(res, "current", "temp_c")

        if isinstance(temp_c, str):  # fallback
            temp_c = 30

        # Logical suggestion
        if "rain" in condition.lower() or temp_c >= 36 or temp_c <= 14:
            dining = "Indoor"
        else:
            dining = "Outdoor"

        return {
            "city": city,
            "condition": condition,
            "temp": temp_c,
            "dining": dining
        }

    except Exception as e:
        print(f"[ERROR] Weather fetch failed for {city}: {e}")
        return {
            "city": city,
            "condition": "Unknown",
            "temp": 30,
            "dining": "Indoor"
        }


# ======== STEP 2: DISH LOGIC ========
def get_iconic_dishes(city):
    # Simulating LLM output with cultural logic
    famous_dishes = {
        "Chennai": ["Idli with Sambar", "Chettinad Chicken", "Filter Coffee"],
        "Delhi": ["Chole Bhature", "Butter Chicken", "Rabri Jalebi"],
        "Kolkata": ["Kosha Mangsho", "Kathi Roll", "Mishti Doi"]
    }
    return famous_dishes.get(city, ["Local Special 1", "Local Special 2", "Local Special 3"])


# ======== STEP 3: RESTAURANT FINDING LOGIC ========
def find_top_restaurants(city, dish):
    # Simulate dynamic search results (replace with real scraping/LLM later)
    database = {
        "Chennai": {
            "Idli with Sambar": "Murugan Idli Shop (4.5⭐)",
            "Chettinad Chicken": "Karaikudi Restaurant (4.6⭐)",
            "Filter Coffee": "Sangeetha Veg (4.4⭐)"
        },
        "Delhi": {
            "Chole Bhature": "Sita Ram Diwan Chand (4.7⭐)",
            "Butter Chicken": "Moti Mahal (4.6⭐)",
            "Rabri Jalebi": "Giani di Hatti (4.5⭐)"
        },
        "Kolkata": {
            "Kosha Mangsho": "6 Ballygunge Place (4.6⭐)",
            "Kathi Roll": "Nizam's (4.5⭐)",
            "Mishti Doi": "Balaram Mullick & Radharaman Mullick (4.8⭐)"
        }
    }
    return database.get(city, {}).get(dish, "Top-rated local eatery")


# ======== STEP 4: BUILD ITINERARY WITH INTELLIGENCE ========
def build_itinerary(city, weather, dishes):
    tour = []
    for i in range(len(meals)):
        dish = dishes[i]
        restaurant = find_top_restaurants(city, dish)

        # Smart location-based adjustment
        if weather["dining"] == "Outdoor" and i == 2:  # dinner usually cooler
            setting = "cozy open-air courtyard"
        elif weather["dining"] == "Outdoor":
            setting = "breezy rooftop or patio"
        else:
            setting = "air-conditioned dining hall"

        meal_text = (
            f"🍽️ {meals[i]}: Savor **{dish}** at *{restaurant}*. "
            f"Perfect for a {setting} experience."
        )
        tour.append(meal_text)
    
    return "\n\n".join(tour)


# ======== STEP 5: COMPOSE FINAL REPORT ========
def format_report(city, weather, dishes, itinerary):
    header = f"📍 **{city.upper()} FOODIE TOUR**"
    weather_info = f"🌤️ *Weather*: {weather['condition']}, {weather['temp']}°C — Suggested: {weather['dining']} dining"
    dishes_list = "\n".join([f"- {d}" for d in dishes])
    
    return f"""
{header}

{weather_info}

🍛 *Local Icons*:
{dishes_list}

📅 *One-Day Foodie Itinerary*:
{itinerary}
""" 


# ======== MASTER FUNCTION ========
def run_foodie_tour():
    for city in cities:
        print("=" * 80)
        weather = get_weather(city)
        dishes = get_iconic_dishes(city)
        itinerary = build_itinerary(city, weather, dishes)
        report = format_report(city, weather, dishes, itinerary)
        print(report)


# ======== RUN MAIN ========
if __name__ == "__main__":
    run_foodie_tour()
