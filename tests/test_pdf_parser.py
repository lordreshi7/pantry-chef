
import pymupdf
import pytest

from app.pdf_parser import *


@pytest.fixture
def sample_pdf(tmp_path):

    pdf_path = tmp_path / "sample.pdf"

    #Create a new PDF document
    with pymupdf.open() as document:

        #Create page 1
        page1 = document.new_page()
        page1.insert_text(
            (72, 72),
            "Vegetable Pulao\nRice, Onion, Peas"
        )
        #Create page 2
        page2 = document.new_page()
        page2.insert_text(
            (72, 72),
            "Dal Tadka\nDal, Tomato, Spices"
        )

        document.save(pdf_path)

    return pdf_path


#Using the sample_pdf path to carry out tests. The pytest.fixture creates a reusable object which can be directly injected into test functions instead of repeatedly calling a function. Reduces duplicity and improves testing environment.
def test_extract_pdf_text(sample_pdf):

    pages = extract_pdf_text(sample_pdf)

    assert len(pages) == 2

    assert pages[0]["page_number"] == 1
    assert "Vegetable Pulao" in pages[0]["text"]
    assert "Rice" in pages[0]["text"]

    assert pages[1]["page_number"] == 2
    assert "Dal Tadka" in pages[1]["text"]

#Test error on missing file.
def test_missing_pdf(tmp_path):

    missing_file = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        extract_pdf_text(missing_file)

#Test error on non-pdf files
def test_invalid_file_extension(tmp_path):

    invalid_file = tmp_path / "sample.txt"

    invalid_file.write_text(
        "This is not a PDF.",
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        extract_pdf_text(invalid_file)

#Test error on empty pdf
def test_empty_pdf_page(tmp_path):

    pdf_path = tmp_path / "empty_page.pdf"

    with pymupdf.open() as document:

        document.new_page()

        document.save(pdf_path)

    pages = extract_pdf_text(pdf_path)

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert pages[0]["text"] == ""

#Test on sample cookbook
def test_sample_cookbook():
    pages = extract_pdf_text("data/cookbooks/Sample Cookbook.pdf")

    print(f"Total pages: {len(pages)}")

    for page in pages[:2]:
        print(f"\nPage {page['page_number']}")
        print("=" * 60)
        print(page["text"])

#Test recipe segmentation
def test_segment_recipes():

    pages = [
        {
            "page_number": 1,
            "text": "RECIPE R001\nVegetable Pulao"
        },
        {
            "page_number": 2,
            "text": "RECIPE R002\nDal Tadka"
        }
    ]

    recipes = segment_recipes(pages)

    assert len(recipes) == 2
    assert recipes[0]["recipe_id"] == "R001"
    assert recipes[0]["page_numbers"] == [1]
    assert recipes[1]["recipe_id"] == "R002"

#Test skipping of pages where recipe is not given
def test_segment_recipes_skip_non_recipe_pages():

    pages = [
        {
            "page_number": 1,
            "text": "Welcome to the cookbook"
        },
        {
            "page_number": 2,
            "text": "RECIPE R001\nVegetable Pulao"
        }
    ]

    recipes = segment_recipes(pages)

    assert len(recipes) == 1
    assert recipes[0]["recipe_id"] == "R001"
    assert recipes[0]["page_numbers"] == [2]

#Test segmentation on empty pages
def test_segment_empty_pages():

    recipes = segment_recipes([])

    assert recipes == []