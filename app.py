from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

MEAL_API_URL = "https://www.themealdb.com/api/json/v1/1/random.php"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    response = requests.get(MEAL_API_URL)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recipe"}), 500
    
    data = response.json()
    
    if not data.get("meals"):
        return jsonify({"error": "No recipes found"}), 404

    meal = data["meals"][0]

    recipe = {
        "name": meal["strMeal"],
        "category": meal["strCategory"],
        "area": meal["strArea"],
        "image": meal["strMealThumb"],
        "instructions": meal["strInstructions"],
        "youtube": meal["strYoutube"],
    }

    return jsonify(recipe)

if __name__ == "__main__":
    app.run(debug=True)
