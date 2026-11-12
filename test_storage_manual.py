from app.storage import *
from app.schemas import *

recipe = Recipe(
    id="R001",
    name="Vegetable Pulao",
    source=Source(
        source_name="Demo Cookbook",
        source_type="pdf"
    )
)

save_recipes([recipe])

loaded = load_recipes()

print(loaded)
print(type(loaded[0]))
print(loaded[0].name)