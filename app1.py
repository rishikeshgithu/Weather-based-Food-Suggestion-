import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import webbrowser

# ========== CONFIGURATION ==========
WEATHER_API_KEY = "9f3ff2a5df2e424ea8110613250706"
ALL_CITIES = ["Chennai", "Delhi", "Kolkata"]

# ========== STYLING ==========
BG_COLOR = "#f9f9f9"
FG_COLOR = "#333333"
ACCENT_COLOR = "#2a9d8f"
FONT_HEAD = ("Segoe UI Semibold", 16)
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
BUTTON_BG = "#2a9d8f"
BUTTON_FG = "#ffffff"
ENTRY_BG = "#ffffff"

# ========== RESTAURANT URL DB ==========
RESTAURANT_LINKS = {
    "Chennai": {
        "Murugan Idli Shop": "https://goo.gl/maps/qkR9kX1U1cM2",
        "Karaikudi Restaurant": "https://goo.gl/maps/xuGKbqDjv1D2",
        "Sangeetha Veg": "https://goo.gl/maps/h3RKe5Yxq6P2"
    },
    "Delhi": {
        "Sita Ram Diwan Chand": "https://goo.gl/maps/d3Xya",
        "Moti Mahal": "https://goo.gl/maps/aUq3B",
        "Giani di Hatti": "https://goo.gl/maps/5Jv8W"
    },
    "Kolkata": {
        "6 Ballygunge Place": "https://goo.gl/maps/y3V7g",
        "Nizam's": "https://goo.gl/maps/Q4dFb",
        "Balaram Mullick & Radharaman Mullick": "https://goo.gl/maps/vzYjK"
    }
}

# ========== CITY FOOD CULTURE ==========
CITY_INTROS = {
    "Chennai": (
        "Chennai, the cultural capital of Tamil Nadu, is famous for its rich South Indian cuisine that "
        "balances spicy and tangy flavors with comfort foods. From fluffy idlis to aromatic filter coffee, "
        "the city offers a delightful culinary experience that celebrates tradition and taste."
    ),
    "Delhi": (
        "Delhi's food culture is a vibrant mix of Mughlai richness and Punjabi zest. The city is renowned for "
        "hearty and flavorful dishes like Butter Chicken and Chole Bhature that have won hearts nationwide."
    ),
    "Kolkata": (
        "Kolkata, the city of joy, boasts a culinary heritage influenced by Bengali tradition and colonial history. "
        "Its cuisine is known for its sweetness and aromatic spices, with specialties like Kosha Mangsho and Mishti Doi."
    )
}

# ========== DISH DESCRIPTIONS ==========
DISH_DESC = {
    "Idli with Sambar": "Steamed rice cakes paired with a spicy lentil stew, a healthy and filling breakfast staple in South India.",
    "Chettinad Chicken": "A fiery and flavorful chicken curry from the Chettinad region, known for its aromatic spices and rich taste.",
    "Filter Coffee": "Strong and aromatic South Indian coffee brewed with a traditional metal filter, perfect to end your meal.",
    "Chole Bhature": "Deep-fried bread served with spicy chickpea curry, a popular Punjabi comfort food, ideal for a power-packed breakfast.",
    "Butter Chicken": "Tender chicken cooked in a creamy tomato-based gravy, a must-try Mughlai delicacy loved all over India.",
    "Rabri Jalebi": "Sweet, fried spiral-shaped dessert soaked in sugar syrup paired with thickened sweetened milk, a perfect dinner dessert.",
    "Kosha Mangsho": "A slow-cooked Bengali spicy mutton curry rich in flavors, perfect for meat lovers seeking authentic taste.",
    "Kathi Roll": "Tandoori chicken wrapped in paratha bread, an iconic Kolkata street food perfect for lunch on-the-go.",
    "Mishti Doi": "Sweetened fermented yogurt, a traditional Bengali dessert served chilled, ideal to finish your dinner."
}

# ========== FUNCTIONS ==========
def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        data = requests.get(url).json()
        condition = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
        norm = condition.lower()
        dining = "Indoor" if "rain" in norm or temp > 35 or temp < 15 else "Outdoor"
        return {"condition": condition, "temp": temp, "dining": dining}
    except:
        return {"condition": "Unknown", "temp": 30, "dining": "Indoor"}

def get_dishes(city):
    return {
        "Chennai": ["Idli with Sambar", "Chettinad Chicken", "Filter Coffee"],
        "Delhi": ["Chole Bhature", "Butter Chicken", "Rabri Jalebi"],
        "Kolkata": ["Kosha Mangsho", "Kathi Roll", "Mishti Doi"]
    }.get(city, ["Local Dish A", "Local Dish B", "Local Dish C"])

def get_restaurant(city, dish):
    db = {
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
    return db.get(city, {}).get(dish, "Top-rated eatery")

def open_map_link(city, restaurant):
    place_name = restaurant.split(" (")[0]
    link = RESTAURANT_LINKS.get(city, {}).get(place_name)
    if link:
        webbrowser.open(link)
    else:
        messagebox.showinfo("Info", "Map link not available for this restaurant.")

def build_itinerary(city, weather, dishes):
    meals = ["Breakfast", "Lunch", "Dinner"]
    meal_times = ["8:00 AM - 9:30 AM", "1:00 PM - 2:30 PM", "7:30 PM - 9:00 PM"]
    intro = (
        f"📍 {city.upper()} FOODIE TOUR\n\n"
        f"{CITY_INTROS.get(city, '')}\n\n"
        f"🌤️ Weather: {weather['condition']}, {weather['temp']}°C\n"
        f"💡 Suggested Dining: {weather['dining']} dining\n\n"
        "⚠️ Tip: Always check the latest weather before heading out to your destinations.\n\n"
    )
    narrative = ""
    for i in range(3):
        dish = dishes[i]
        place = get_restaurant(city, dish)
        setting = "breezy rooftop or patio" if weather["dining"] == "Outdoor" else "cozy indoor hall or lounge"
        dish_info = DISH_DESC.get(dish, "A delicious local specialty.")
        narrative += (
            f"🍽️ {meals[i]} ({meal_times[i]}):\n"
            f"Enjoy **{dish}** at *{place}*.\n"
            f"Recommended setting: {setting}\n"
            f"About the dish: {dish_info}\n"
            "🕒 Tip: Try to arrive during non-peak hours for a relaxed experience.\n\n"
        )
    narrative += "Enjoy your foodie adventure! 🍴"
    return intro + narrative

def generate_tour():
    output.config(state="normal")
    output.delete("1.0", tk.END)
    selected_cities = [city for city, var in city_vars.items() if var.get() == 1]
    if not selected_cities:
        messagebox.showwarning("Selection Required", "Please select at least one city.")
        return
    for city in selected_cities:
        weather = get_weather(city)
        dishes = get_dishes(city)
        plan = build_itinerary(city, weather, dishes)
        output.insert(tk.END, plan + "\n" + "="*90 + "\n\n")
    output.config(state="disabled")
    status_var.set(f"Generated tours for {', '.join(selected_cities)}")

def on_restaurant_click(event):
    idx = output.index(f"@{event.x},{event.y}").split('.')[0]
    line = output.get(f"{idx}.0", f"{idx}.end").strip()
    if "at *" in line:
        for city in ALL_CITIES:
            if city.upper() in output.get("1.0", "end"):
                restaurant_start = line.find("at *") + 4
                restaurant_end = line.find("*.", restaurant_start)
                if restaurant_end == -1:
                    restaurant_end = len(line)
                restaurant_name = line[restaurant_start:restaurant_end]
                open_map_link(city, restaurant_name)
                break

# ========== GUI ==========
root = tk.Tk()
root.title("Smart Foodie Tour Planner")
root.geometry("850x700")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Title Frame
title_frame = tk.Frame(root, bg=BG_COLOR)
title_frame.pack(fill='x', pady=(15, 10))
title_lbl = tk.Label(title_frame, text="Smart Foodie Tour Planner", font=FONT_HEAD, bg=BG_COLOR, fg=ACCENT_COLOR)
title_lbl.pack()

# Instructions
desc_lbl = tk.Label(root, text="Select cities and generate customized weather-aware foodie tours.",
                    font=FONT_BODY, bg=BG_COLOR, fg=FG_COLOR)
desc_lbl.pack(pady=(0, 15))

# City selection frame
city_frame = ttk.LabelFrame(root, text="Choose Cities", padding=(10, 10))
city_frame.pack(fill='x', padx=20)

city_vars = {}
for city in ALL_CITIES:
    var = tk.IntVar()
    chk = ttk.Checkbutton(city_frame, text=city, variable=var)
    chk.pack(anchor='w', pady=2)
    city_vars[city] = var

# Generate button
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=15)
generate_btn = tk.Button(btn_frame, text="Generate Foodie Tour", command=generate_tour,
                         bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BODY, relief='flat', padx=20, pady=8, cursor="hand2")
generate_btn.pack()

# Output display (read-only)
output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 11), bg=ENTRY_BG, fg=FG_COLOR, height=25, state="disabled")
output.pack(fill='both', padx=20, pady=(0, 10), expand=True)

# Status bar
status_var = tk.StringVar()
status_var.set("Select cities and click 'Generate Foodie Tour'")
status_bar = tk.Label(root, textvariable=status_var, font=FONT_SMALL, bg="#e0e0e0", fg="#555555", anchor='w')
status_bar.pack(fill='x', side='bottom')

root.mainloop()
