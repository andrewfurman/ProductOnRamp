import os
import json
from openai import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def summarize_plan_gpt(product_id):
    # Create a database engine and session
    engine = create_engine(os.environ['DATABASE_URL'])
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Retrieve the product from the database
        product = session.query(Product).get(product_id)

        if not product:
            print(f"Product with ID {product_id} not found.")
            return

        # Prepare the ChatGPT API request
        payload = {
            "model": "gpt-4o-mini",  # mini
            # "model": "gpt-4o-2024-08-06",  # supports structured output 
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that uses the text in a Summary of Benefits Coverage for a health insurance plan to extract the product name, line of business, and a summary of what the product covers."},
                {"role": "user", "content": f"Please analyze the following health insurance plan. The plan URL is: {product.url}\n\nThe plan summary of benefits is:\n\n{product.summary_of_benefits}\n\nBased on this information, provide the product name, line of business (lob), and a brief coverage summary."}
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "health_insurance_summary",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "The name of the health insurance product. Formatted like this example: Sm Grp Horizon Advantage EPO Gold 100 $40/$60 BlueCard"
                            },
                            "line_of_business": {
                                "type": "string",
                                "description": "The line of business for the health insurance product. The name should be one of the following: Large Group (100+), Midsize Group (51-99), Small Group (2-50), Individuals and Families, Medicare Advantage, Medicaid.  In the URL SMG = Small Group, MIDSIZE = Midsize, "
                            },
                            "coverage_summary": {
                                "type": "string",
                                "description": "A comprehensive summary of the Health Insurance Plan based on the provided Summary of Benefits document. Include the coverage period, types of coverage, plan type, and contact information. Detail deductibles, out-of-pocket maximums, copayments, coinsurance, covered services, and exclusions for both in network and out of network care. Highlight prior authorization requirements, service limitations, provider network details, and how out-of-network coverage works. Include information on continuation of coverage, grievance processes, and whether the plan meets Minimum Essential Coverage and Minimum Value Standards. Provide example scenarios to illustrate coverage for common medical events. Format this description as markdown so that it is easy to quickly scan."
                            }
                        },
                        "required": ["product_name", "line_of_business", "coverage_summary"],
                        "additionalProperties": False
                    }
                }
            }
        }

        # Send request to ChatGPT API
        response = client.chat.completions.create(**payload)

        # Extract the summary from the response
        result = json.loads(response.choices[0].message.content)

        # Update the product in the database
        product.name = result['product_name']
        product.line_of_business = result['line_of_business']
        product.coverage_summary = result['coverage_summary']
        session.commit()

        print(f"Successfully updated product ID {product_id}")
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()
        return None

    finally:
        session.close()

# Example usage:
# result = summarize_plan_gpt(1)  # Where 1 is the ID of the product you want to summarize