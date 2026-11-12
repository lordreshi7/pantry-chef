
from app.storage import *
from app.schemas import *


#Create Sample Recipe to test functionality
def create_sample_recipe():
    return Recipe(
        id="R001",
        name="Vegetable Pulao",
        cuisine="Indian",
        servings=2,
        ingredients=[
            Ingredient(
                name="Rice",
                quantity=200,
                unit="grams"
            ),
            Ingredient(
                name="Onion",
                quantity=1,
                unit="nos"
            )
        ],
        source=Source(
            source_name="Demo Cookbook",
            source_type="pdf",
            page_number=[12]
        )
    )

#Testing saving and loading
def test_save_and_load_recipes(tmp_path):

    #Saving recipe in tmp_path so that main recipe database is not disturbed
    file_path = tmp_path / "recipes.json"

    recipe = create_sample_recipe()

    #Save
    save_recipes([recipe], file_path)

    #Load
    loaded_recipes = load_recipes(file_path)

    assert len(loaded_recipes) == 1
    assert loaded_recipes[0] == recipe
    assert isinstance(loaded_recipes[0], Recipe)
    assert isinstance(loaded_recipes[0].ingredients[0], Ingredient)

#Testing loading from non-existing/empty file
def test_load_missing_file(tmp_path):
    file_path = tmp_path / "missing.json"

    recipes = load_recipes(file_path)

    assert recipes == []

#Test saving multiple recipes
def test_save_multiple_recipes(tmp_path):
    file_path = tmp_path / "recipes.json"

    recipe1 = create_sample_recipe()

    recipe2 = Recipe(
        id="R002",
        name="Dal Tadka",
        source=Source(
            source_name="Demo Cookbook",
            source_type="pdf"
        )
    )

    save_recipes([recipe1, recipe2], file_path)

    loaded_recipes = load_recipes(file_path)

    assert len(loaded_recipes) == 2
    assert loaded_recipes[0].id == "R001"
    assert loaded_recipes[1].id == "R002"
