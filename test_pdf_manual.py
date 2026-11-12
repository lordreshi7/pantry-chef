from app.pdf_parser import *

pages = extract_pdf_text(
    "data/cookbooks/Sample Cookbook.pdf"
)

recipe_blocks = segment_recipes(pages)

print(f"Total pages: {len(pages)}")
print(f"Total recipes: {len(recipe_blocks)}")

for recipe in recipe_blocks:
    print(
        f"Recipe ID: {recipe['recipe_id']} | "
        f"Pages: {recipe['page_numbers']}"
    )
