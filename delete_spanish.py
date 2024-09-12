# this function will loop through all the products and delete the ones that are in Spanish. Plans in spanish can be identified by those that contain "NOD_ES-US" in the plan_url column

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product
import os

def delete_spanish_products():
    # Create a database engine and session
    engine = create_engine(os.environ['DATABASE_URL'])
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Query for products with "NOD_ES-US" in the url
        spanish_products = session.query(Product).filter(Product.url.like("%NOD_ES-US%")).all()

        if not spanish_products:
            print("No Spanish products found.")
            return

        count = 0
        for product in spanish_products:
            print(f"Deleting Spanish product ID: {product.id}")
            print(f"URL: {product.url}")  # Added this line to print the URL
            session.delete(product)
            count += 1

        # Commit the changes to the database
        session.commit()
        print(f"Successfully deleted {count} Spanish products.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    delete_spanish_products()