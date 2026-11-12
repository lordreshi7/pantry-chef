
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
        name="Rice",
        quantity=2,
        unit="cups"
    )

    pantry2 = PantryItem(
        name="Soy Sauce",
        quantity="250", #Intentionally adding number as str to check type casting by pydantic
        unit="ml"
    )

    pantry3 = PantryItem(
        name="Cookies"
    )

    with pytest.raises(ValidationError):
        PantryItem(
            name = "Tomatoes",
            quantity=-4,
            unit="grams",
        )

    with pytest.raises(ValidationError):
        PantryItem(
            name="Rice",
            quantity=0,
            unit="cups"
        )

    #Test normal input
    assert pantry1.name == "Rice"
    assert pantry1.quantity == 2.0
    assert pantry1.unit == "cups"

    #Test automatic type conversion
    assert pantry2.quantity == 250.0
    assert isinstance(pantry2.quantity, float)
    assert pantry2.unit == "ml"

    #Test optional fields
    assert pantry3.quantity is None
    assert pantry3.unit is None

    #Test invalid input
    with pytest.raises(ValidationError):
        PantryItem(
            name="Tomatoes",
            quantity="four",
            unit="count"
        )



#Testing User Profile
def test_UserProfile():

    user1 = UserProfile(
        allergies = ['Peanuts', 'Raspberry'],
        dietary_preference = ['Ketogenic', 'Pescatarian'],
        skill_level = 'intermediate',
        max_cooking_time_mins = 30,
        pantry = [
            PantryItem(
                name = 'Rice', quantity = 250, unit = 'grams'
            ),
            PantryItem(
                name = 'Dal', quantity = 3, unit = 'cups'
            ),
            PantryItem(
                name = 'Onion', quantity = 1, unit = 'nos'
            )
        ]
    )

    user2 = UserProfile(
            skill_level = 'beginner',
            max_cooking_time_mins = 60,
            pantry = [
                PantryItem(
                    name = 'Beef', quantity = 100, unit = 'pounds'
                ),
                PantryItem(
                    name = 'Tomato Paste', quantity = 100, unit = 'grams'
                ),
                PantryItem(
                    name = 'Chicken Stock', quantity = 1, unit = 'cup'
                )
            ]
        )

    #Verify first user profile
    assert user1.allergies == ["Peanuts", "Raspberry"]
    assert user1.dietary_preference == [
        "Ketogenic",
        "Pescatarian"
    ]
    assert user1.skill_level == "intermediate"
    assert user1.max_cooking_time_mins == 30

    #Verify pantry contents
    assert len(user1.pantry) == 3
    assert user1.pantry[0].name == "Rice"
    assert user1.pantry[0].quantity == 250.0
    assert user1.pantry[0].unit == "grams"

    #Verify second user profile
    assert user2.skill_level == "beginner"
    assert user2.max_cooking_time_mins == 60
    assert len(user2.pantry) == 3

    #Verify default fields
    assert user2.allergies == []
    assert user2.dietary_preference == []

#Test for invalid user level
def test_invalid_skill_level():
    with pytest.raises(ValidationError):
        UserProfile(
            skill_level="expert"
        )

#Test for invalid cooking time
def test_invalid_cooking_time():
    with pytest.raises(ValidationError):
        UserProfile(
            max_cooking_time_mins=-30
        )

    with pytest.raises(ValidationError):
        UserProfile(
            max_cooking_time_mins=0
        )

#Check for unexpected field when creating Ingredient item
def test_unexpected_ingredient_field():
    with pytest.raises(ValidationError):
        Ingredient(
            name="Rice",
            quantity=200,
            unit="grams",
            unexpected_field="test"
        )

#Check for unexpected field when creating Pantry item
def test_unexpected_pantry_field():
    with pytest.raises(ValidationError):
        PantryItem(
            name="Rice",
            quantity=200,
            units="grams"
        )

#Checking for nested items
def test_unexpected_nested_field():
    with pytest.raises(ValidationError):
        Recipe(
            id="R001",
            name="Vegetable Pulao",
            ingredients=[
                {
                    "name": "Rice",
                    "quantity": 200,
                    "unit": "grams",
                    "unexpected_field": "test"
                }
            ],
            source=Source(
                source_name="Demo Cookbook",
                source_type="pdf"
            )
        )

#Testing ingredient size

def test_ingredient_size():
    ingredient = Ingredient(
        name="Onion",
        quantity=1,
        unit="count",
        size="medium",
        preparation="sliced"
    )

    assert ingredient.name == "Onion"
    assert ingredient.quantity == 1.0
    assert ingredient.unit == "count"
    assert ingredient.size == "medium"
    assert ingredient.preparation == "sliced"
    assert ingredient.optional is False

#Testing equipment size
def test_equipment():
    equipment = Equipment(
        name="Saucepan",
        size_relative="medium",
        size_abs="2 L",
        material="stainless steel"
    )

    assert equipment.name == "Saucepan"
    assert equipment.size_relative == "medium"
    assert equipment.size_abs == "2 L"
    assert equipment.material == "stainless steel"

#Testing optional fields for Equipment
def test_equipment_optional_fields():
    equipment = Equipment(
        name="Cutting board"
    )

    assert equipment.name == "Cutting board"
    assert equipment.size_relative is None
    assert equipment.size_abs is None
    assert equipment.material is None
