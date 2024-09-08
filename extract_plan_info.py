import requests
from io import BytesIO
import pdfplumber
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product
import os

def format_markdown_table(table):
    if not table:
        return ""

    # Calculate the maximum width for each column
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]

    # Format the header
    header = "| " + " | ".join(str(cell).ljust(width) for cell, width in zip(table[0], col_widths)) + " |"
    separator = "|" + "|".join("-" * 3 for _ in col_widths) + "|"

    # Format the rows
    rows = []
    for row in table[1:]:
        formatted_row = "| " + " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths)) + " |"
        rows.append(formatted_row)

    # Combine all parts
    return "\n".join([header, separator] + rows) + "\n"

def extract_text_from_pdf(url: str) -> str:
    response = requests.get(url)
    text = ""

    with pdfplumber.open(BytesIO(response.content)) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            # Add Page number marker
            page_marker = f"\n🅿️ Start Page {page_num}\n"
            text += page_marker

            # Extract tables from the page
            tables = page.extract_tables()

            if tables:
                for table in tables:
                    # Use our custom function to format the table
                    markdown_table = format_markdown_table(table)
                    text += "\n" + markdown_table + "\n"

            # Extract and add remaining text
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

def process_and_save_pdf_content(product_id: int):
    # Create a database engine and session
    engine = create_engine(os.environ['DATABASE_URL'])
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Fetch the product from the database
        product = session.query(Product).get(product_id)
        
        if not product:
            print(f"Product with ID {product_id} not found.")
            return

        # Extract text from the PDF
        pdf_content = extract_text_from_pdf(product.url)

        # Update the summary_of_benefits field
        product.summary_of_benefits = pdf_content

        # Commit the changes to the database
        session.commit()
        print(f"Successfully updated summary of benefits for product ID {product_id}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()

    finally:
        session.close()