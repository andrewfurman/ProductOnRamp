from flask import Flask, redirect, url_for, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models import Base, Product
import os
import time
from extract_plan_info import process_and_save_pdf_content
from summarize_gpt import summarize_plan_gpt
from detailed_attributes_gpt import extract_product_details

app = Flask(__name__)
engine = create_engine(os.environ['DATABASE_URL'])
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    return SessionLocal()

def get_product_with_retry(session, product_id, max_retries=3, retry_delay=1):
    for attempt in range(max_retries):
        try:
            return session.query(Product).get(product_id)
        except OperationalError as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                session.rollback()
            else:
                raise e

def truncate_summary(summary, lines=5):
    if summary:
        return '\n'.join(summary.split('\n')[:lines])
    return ''

@app.route('/')
def products():
    session = get_db_session()
    try:
        products = session.query(Product).all()
        for product in products:
            product.summary_preview = truncate_summary(product.summary_of_benefits)
        return render_template('products.html', products=products)
    except OperationalError:
        return render_template('products.html', products=[])
    finally:
        session.close()

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    session = get_db_session()
    try:
        product = get_product_with_retry(session, product_id)
        if product:
            return render_template('product_detail.html', product=product)
        else:
            return redirect(url_for('products'))
    except OperationalError:
        return redirect(url_for('products'))
    finally:
        session.close()

@app.route('/add_products', methods=['POST'])
def add_products():
    urls = request.form.get('urls', '').split(',')
    session = get_db_session()
    new_product_ids = []
    try:
        for url in urls:
            url = url.strip()
            if url:
                # Check if the URL already exists in the database
                existing_product = session.query(Product).filter(Product.url == url).first()
                if existing_product:
                    print(f"Product with URL {url} already exists. Skipping.")
                    continue
                
                new_product = Product(url=url)
                session.add(new_product)
                session.flush()  # This will assign an ID to the new product
                new_product_ids.append(new_product.id)

        session.commit()  # Commit the new products to the database

        # Process the PDFs and generate summaries for the newly added products
        for product_id in new_product_ids:
            try:
                process_and_save_pdf_content(product_id)
                summarize_plan_gpt(product_id)  # Call summarize_plan_gpt for each new product
                extract_product_details(product_id)  # Call extract_product_details for each new product
            except Exception as e:
                print(f"Error processing product ID {product_id}: {str(e)}")

    except Exception as e:
        session.rollback()
        print(f"Error adding products: {str(e)}")
    finally:
        session.close()

    return redirect(url_for('products'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    session = get_db_session()
    try:
        product = session.query(Product).get(product_id)
        if product:
            session.delete(product)
            session.commit()
    except OperationalError:
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('products'))

from flask import redirect, url_for

@app.route('/generate_summary/<int:product_id>', methods=['POST'])
def generate_summary(product_id):
    try:
        # Call summarize_plan_gpt with the product ID
        summary = summarize_plan_gpt(product_id)
        
        if summary:
            # Redirect to the product detail page
            return redirect(url_for('product_detail', product_id=product_id))
        else:
            return jsonify({"success": False, "error": "Failed to generate summary"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/generate_detailed_attributes/<int:product_id>', methods=['POST'])
def generate_detailed_attributes(product_id):
    try:
        # Call the extract_product_details function
        result = extract_product_details(product_id)
        
        if result:
            # If successful, redirect to the product detail page
            return redirect(url_for('product_detail', product_id=product_id))
        else:
            # If there was an error, return a JSON response
            return jsonify({"success": False, "error": "Failed to generate detailed attributes"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/detailed_products_list')
def detailed_products_list():
    session = get_db_session()
    try:
        products = session.query(Product).all()
        return render_template('detailed_products_list.html', products=products)
    except OperationalError:
        return render_template('detailed_products_list.html', products=[])
    finally:
        session.close()

@app.route('/extract_all')
def extract_all():
    session = get_db_session()
    try:
        products = session.query(Product).all()
        processed_count = 0

        for product in products:
            if product.summary_of_benefits is None:
                try:
                    process_and_save_pdf_content(product.id)
                    processed_count += 1
                except Exception as e:
                    print(f"Error processing product ID {product.id}: {str(e)}")

        return f"Processed {processed_count} products with null Summary of Benefits.", 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)