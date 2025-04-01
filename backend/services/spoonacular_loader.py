import os
import requests
import csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")

PROCESSED_TITLES = set()
CSV_FILE = "spoonacular_meals.csv"

# Load existing titles to avoid duplicates
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            PROCESSED_TITLES.add(row["name"])


def fetch_recipe_ids(query="", number=50):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "number": number,
        "query": query
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return [item["id"] for item in response.json().get("results", [])]


def fetch_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": API_KEY,
        "includeNutrition": True
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_meal_info(recipe):
    title = recipe.get("title", "Unknown")
    ingredients_list = [i["name"] for i in recipe.get("extendedIngredients", [])]
    ingredients = ", ".join(ingredients_list)

    nutrients = recipe.get("nutrition", {}).get("nutrients", [])
    nutrition_map = {n["name"]: n["amount"] for n in nutrients}

    return {
        "name": title,
        "ingredients": ingredients,
        "calories": int(nutrition_map.get("Calories", 0)),
        "protein": int(nutrition_map.get("Protein", 0)),
        "fat": int(nutrition_map.get("Fat", 0)),
        "carbs": int(nutrition_map.get("Carbohydrates", 0)),
    }


def save_to_csv(meals):
    is_new = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["name", "ingredients", "calories", "protein", "fat", "carbs"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new:
            writer.writeheader()
        for meal in meals:
            writer.writerow(meal)


def load_meals():
    search_terms = [
        "salad", "pasta", "chicken", "beef", "soup", "stir fry", "bowl",
        "breakfast", "lunch", "dinner", "vegan", "tofu", "wrap", "seafood",
        "grilled", "rice", "curry", "burrito", "pizza", "noodle"
    ]

    all_new_meals = []

    for term in search_terms:
        print(f"Fetching recipes for: {term}")
        recipe_ids = fetch_recipe_ids(query=term, number=25)
        for recipe_id in recipe_ids:
            try:
                recipe = fetch_recipe_details(recipe_id)
                meal_data = extract_meal_info(recipe)
                if meal_data["name"] not in PROCESSED_TITLES:
                    all_new_meals.append(meal_data)
                    PROCESSED_TITLES.add(meal_data["name"])
            except Exception as e:
                print(f"Error processing recipe ID {recipe_id}: {e}")

    print(f"Saving {len(all_new_meals)} new meals to CSV...")
    save_to_csv(all_new_meals)
    print("Done.")


if __name__ == "__main__":
    load_meals()