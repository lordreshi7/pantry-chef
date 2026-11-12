import json
from pathlib import Path
from pydantic import TypeAdapter
from app.schemas import *

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of our recipe database
RECIPE_FILE = PROJECT_ROOT / "data" / "recipes.json"

# Pydantic adapter for validating a list of Recipe objects
recipe_list_adapter = TypeAdapter(list[Recipe])


#Getting a list of parsed recipe objects, storing them to our data.json
def save_recipes(recipes: list[Recipe], file_path: Path = RECIPE_FILE) -> None:
    """
    Save a list of Recipe objects to a JSON file.
    """

    #Ensure the data directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    #Convert Pydantic models into JSON-compatible dictionaries
    recipe_data = [
        recipe.model_dump(mode="json")
        for recipe in recipes
    ]

    #Write data to JSON
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(recipe_data, file, indent=4, ensure_ascii=False)
        print("Recipe stored!")


#Loading recipes back into list of Recipes
def load_recipes(file_path: Path = RECIPE_FILE) -> list[Recipe]:
    """
    Load recipes from JSON and validate them using Pydantic.
    """

    #If the file doesn't exist, return an empty list
    if not file_path.exists():
        return []

    #Read JSON data
    with file_path.open("r", encoding="utf-8") as file:
        recipe_data = json.load(file)

    #Validate the JSON and reconstruct Recipe objects
    recipes = recipe_list_adapter.validate_python(recipe_data)

    return recipes

