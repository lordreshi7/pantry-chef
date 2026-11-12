
from pydantic import BaseModel, Field
from typing import Literal

#Ingredient from recipe
class Ingredient(BaseModel):
    name: str
    quantity: float | None = None
    unit: str | None = None
    optional: bool = False
    preparation: str | None = None

#Pantry Items that User provides. Keeping them as structured objects allows the llm to update values in structured manner instead of running evaluations everytime the user updates pantry items.
class PantryItem(BaseModel):
    name : str
    quantity : float | None = Field(default = None, gt = 0)
    unit: str | None = None

#Equipment mentioned in recipe
class Equipment(BaseModel):
    name: str
    quantity: float | None = None
    unit: str | None = None
    optional: bool = False
    preparation: str | None = None
    size: str | None = None

#Step from recipe
class Step(BaseModel):
    step_number: int
    instruction: str
    duration_mins: int | None = None

#Recipe Source
class Source(BaseModel):
    source_name: str
    source_type: str
    source_url: str | None = None
    page_number: list[int] = Field(default_factory=list)

#THE Recipe
class Recipe(BaseModel):
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
class UserProfile(BaseModel):
    allergies : list[str] = Field(default_factory=list)
    dietary_preference : list[str] = Field(default_factory=list)
    skill_level : Literal[
        'beginner', 'intermediate', 'advanced'
    ] | None = None
    servings: int | None = None
    max_cooking_time_mins : int | None = Field(default = None, gt = 0)
    pantry : list[PantryItem] | None = None
    available_equipment : list[Equipment] = Field(default_factory=list)

    