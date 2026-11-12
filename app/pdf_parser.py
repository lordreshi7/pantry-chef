
from pathlib import Path
import pymupdf
import re


def extract_pdf_text(pdf_path: str | Path) -> list[dict]:
    """
    Extract text from a PDF document page by page.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of dictionaries containing the page number and extracted text.
    """

    pdf_path = Path(pdf_path)

    #Check whether the file exists
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    #Check whether the file is a PDF
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    extracted_pages = []

    #Open the PDF document. Opened using 'with' keyword so that pdf is closed even if an error is raised.
    with pymupdf.open(pdf_path) as document:

        for page_index, page in enumerate(document):

            #Extract text from the current page
            text = page.get_text("text").strip()

            #Store page number and text
            extracted_pages.append({
                "page_number": page_index + 1,
                "text": text
            })

    return extracted_pages

#Recipe Segmentation for better text injection for LLM extraction

import re


def segment_recipes(pages: list[dict]) -> list[dict]:
    """
    Identify individual recipes from extracted PDF pages.

    Initial implementation:
    Currrently assumes one recipe per page and a recipe ID in the format R001, R002, etc.
    """

    recipe_blocks = []

    for page in pages:

        text = page["text"]

        # Find the recipe ID
        match = re.search(
            r"\bRECIPE\s+(R\d+)\b",
            text
        )

        # Skip pages without a recipe ID
        if match is None:
            continue

        recipe_id = match.group(1)

        recipe_blocks.append({
            "recipe_id": recipe_id,
            "page_numbers": [page["page_number"]],
            "text": text
        })

    return recipe_blocks
