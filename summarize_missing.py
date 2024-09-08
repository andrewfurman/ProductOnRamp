from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from models import Product
from summarize_gpt import summarize_plan_gpt
import os

def summarize_missing_products():
    # Create a database engine and session
    engine = create_engine(os.environ['DATABASE_URL'])
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Query for products with null name or summary
        products = session.query(Product).filter(or_(Product.name == None, Product.summary_of_benefits == None)).all()

        if not products:
            print("No products found with missing name or summary.")
            return

        for product in products:
            print(f"Summarizing product ID: {product.id}")
            try:
                summarize_plan_gpt(product.id)
                print(f"Successfully summarized product ID: {product.id}")
            except Exception as e:
                print(f"Error summarizing product ID {product.id}: {str(e)}")

        print("Finished summarizing all missing products.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    summarize_missing_products()