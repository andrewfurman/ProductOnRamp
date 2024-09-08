from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product
from detailed_attributes_gpt import extract_product_details
import os

def details_missing():
    # Create a database engine and session
    engine = create_engine(os.environ['DATABASE_URL'])
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Query for products with null in_network_individual_deductible
        products = session.query(Product).filter(Product.in_network_individual_deductible == None).all()

        if not products:
            print("No products found with missing in_network_individual_deductible.")
            return

        for product in products:
            print(f"Extracting details for product ID: {product.id}")
            try:
                extract_product_details(product.id)
                print(f"Successfully extracted details for product ID: {product.id}")
            except Exception as e:
                print(f"Error extracting details for product ID {product.id}: {str(e)}")

        print("Finished extracting details for all products with missing in_network_individual_deductible.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    details_missing()