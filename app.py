from flask import Flask, render_template, request, jsonify
import http.client
import json

app = Flask(__name__)

# Spoonacular API details
API_HOST = "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
API_KEY = "d9045911f0msha288e25cc902400p1dd65ejsn15a51e9fa5c0"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    conn.request("GET", "/recipes/random?tags=vegetarian,dessert&number=1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    recipe_data = json.loads(data.decode("utf-8"))
    
    if "recipes" not in recipe_data or not recipe_data["recipes"]:
        return jsonify({"error": "No recipes found"}), 404
    
    recipe = recipe_data["recipes"][0]
    
    recipe_details = {
        "title": recipe["title"],
        "image": recipe["image"],
        "instructions": recipe["instructions"] if "instructions" in recipe else "No instructions available.",
        "source": recipe["sourceUrl"]
    }
    
    return jsonify(recipe_details)

if __name__ == "__main__":
    app.run(debug=True)
