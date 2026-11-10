
from app.schemas import *
from pydantic import ValidationError
import pytest


def test_ingredient():
    ingredient = Ingredient(name="Rice")

    assert ingredient.name == "Rice"
    assert ingredient.quantity is None


def test_source():
    source = Source(
        source_name="Demo Cookbook",
        source_type="pdf"
    )

    assert source.page_number == []


def test_recipe():
    recipe = Recipe(
        id="R001",
        name="Vegetable Pulao",
        source=Source(
            source_name="Demo Cookbook",
            source_type="pdf"
        )
    )

    assert recipe.name == "Vegetable Pulao"
    assert recipe.ingredients == []
    assert recipe.steps == []


def test_serialization():
    recipe = Recipe(
        id="R001",
        name="Vegetable Pulao",
        source=Source(
            source_name="Demo Cookbook",
            source_type="pdf"
        )
    )

    data = recipe.model_dump()

    reconstructed = Recipe.model_validate(data)

    assert reconstructed == recipe

#Invalid test. We are storing 'rice' and asserting that name should be 'wheat'. This test will fail. Please comment out after trial.
'''
def test_invalid_ingredient():
    ingredient = Ingredient(
        name="Rice",
        quantity=200
    )

    assert ingredient.name == "Wheat"
'''

#This will give validation error
def test_invalid_ingredient_quantity():
    with pytest.raises(ValidationError):
        Ingredient(
            name="Rice",
            quantity="two hundred",
            unit="grams"
        )

#Ingredient Quantity test
def test_empty_ingredient_quantity():
    with pytest.raises(ValidationError):
        Ingredient(
            name='Orange',
            quantity='',
            unit='nos'
        )

#Test whether all recipes implement their own list initialization or not
def test_recipe_lists_are_independent():
    recipe1 = Recipe(
        id = 'R0001',
        name = 'Pizza',
        source = Source(
            source_name = 'Demo',
            source_type = 'pdf'
        )
    )

    recipe2 = Recipe(
        id = 'R0002',
        name = 'Pasta',
        source = Source(
            source_name = 'Demo',
            source_type = 'pdf'
        )
    )

    recipe1.ingredients.append(
        Ingredient(name='Flour')
    )

    assert len(recipe1.ingredients) == 1
    assert len(recipe2.ingredients) == 0

#Testing if pydantic flags when mandatory fields are excluded
def test_missing_ingredient_name():
    with pytest.raises(ValidationError):
        Ingredient(
            quantity=200,
            unit="grams"
        )


#Testing Pantry Item
def test_PantryItem():
    pantry1 = PantryItem(
        name = 'Rice',
        quantity = 2,
        unit = 'cups'
    )

    pantry2 = PantryItem(
        name = 'Soy Sauce',
        quantity = '250', #Intentionally adding number in string to check type cast
        units = 'ml'
    )

    pantry3 = PantryItem(
        name = 'Cookies'
    )

    with pytest.raises(ValidationError):
        PantryItem(
            name = 'Tomatoes',
            quantity = 'four',
            unit = 'nos'
        )

    assert pantry3.quantity == None


#Testing User Profile
def test_UserProfile():

    user1 = UserProfile(
        allergies = ['Peanuts', 'Raspberry'],
        dietary_preference = ['Ketogenic', 'Pescatarian'],
        skill_level = 'intermediate',
        max_cooking_time_mins = 30,
        pantry = [
            PantryItem(
                name = 'Rice', quantity = 250, units = 'grams'
            ),
            PantryItem(
                name = 'Dal', quantity = 3, units = 'cups'
            ),
            PantryItem(
                name = 'Onion', quantity = 1, units = 'nos'
            )
        ]
    )

    user2 = UserProfile(
            skill_level = 'beginner',
            max_cooking_time_mins = 60,
            pantry = [
                PantryItem(
                    name = 'Beef', quantity = 100, units = 'pounds'
                ),
                PantryItem(
                    name = 'Tomato Paste', quantity = 100, units = 'grams'
                ),
                PantryItem(
                    name = 'Chicken Stock', quantity = 1, units = 'cup'
                )
            ]
        )
