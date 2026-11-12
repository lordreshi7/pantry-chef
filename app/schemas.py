
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

#Disabling pydantic to ignore wrong attributes being passed in tests or production
class PantryBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

#Ingredient from recipe
class Ingredient(PantryBaseModel):
    name: str
    quantity: float | None = None
    unit: str | None = None
    optional: bool = False
    preparation: str | None = None
    size: str | None = None

#Pantry Items that User provides. Keeping them as structured objects allows the llm to update values in structured manner instead of running evaluations everytime the user updates pantry items.
class PantryItem(PantryBaseModel):
    name : str
    quantity : float | None = Field(default = None, gt = 0)
    unit: str | None = None

#Equipment mentioned in recipe
class Equipment(PantryBaseModel):
    name: str
    size_relative: str | None = None
    size_abs: str | None = None
    material: str | None = None

#Step from recipe
class Step(PantryBaseModel):
    step_number: int
    instruction: str
    duration_mins: int | None = None

#Recipe Source
class Source(PantryBaseModel):
    source_name: str
    source_type: str
    source_url: str | None = None
    page_number: list[int] = Field(default_factory=list)

#THE Recipe
class Recipe(PantryBaseModel):
    id: str
    name: str
    cuisine: str | None = None
    servings: int | None = None
    prep_time_mins: int | None = None
    cook_time_mins: int | None = None
    difficulty: str | None = None
    dietary_classification : str | None = None
    ingredients: list[Ingredient] = Field(default_factory=list)
    steps: list[Step] = Field(default_factory=list)
    equipment: list[Equipment] = Field(default_factory=list)
    allergens: list[str] = Field(default_factory=list)
    source: Source


#User Profile - attributes about the user that they self-describe based on questions asked by the agent.
class UserProfile(PantryBaseModel):
    allergies : list[str] = Field(default_factory=list)
    dietary_preference : list[str] = Field(default_factory=list)
    skill_level : Literal[
        'beginner', 'intermediate', 'advanced'
    ] | None = None
    servings: int | None = None
    max_cooking_time_mins : int | None = Field(default = None, gt = 0)
    pantry : list[PantryItem] | None = None
    available_equipment : list[Equipment] = Field(default_factory=list)

    