# detailed_attributes_gpt.py

# This file has a function called extract_product_details. This function will receive a ID for a product as the only parameter. Then it will make a request to open AI and set all of the values for this product in the database that are not set by the summarize_plan_gpt function

import os
import json
from openai import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def extract_product_details(product_id):
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
            "model": "gpt-4o-mini",  # supports structured output 
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that extracts detailed attributes from health insurance plan coverage summaries."},
                {"role": "user", "content": f"Please analyze the following health insurance plan coverage summary and extract detailed attributes:\n\n{product.coverage_summary}"}
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "health_insurance_details",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "in_network_individual_deductible": {
                                "type": "number",
                                "description": "The individual deductible amount for in-network services"
                            },
                            "in_network_family_deductible": {
                                "type": "number",
                                "description": "The family deductible amount for in-network services"
                            },
                            "out_of_network_individual_deductible": {
                                "type": "number",
                                "description": "The individual deductible amount for out-of-network services"
                            },
                            "out_of_network_family_deductible": {
                                "type": "number",
                                "description": "The family deductible amount for out-of-network services"
                            },
                            "in_network_individual_oop_limit": {
                                "type": "number",
                                "description": "The individual out-of-pocket limit for in-network services"
                            },
                            "in_network_family_oop_limit": {
                                "type": "number",
                                "description": "The family out-of-pocket limit for in-network services"
                            },
                            "out_of_network_individual_oop_limit": {
                                "type": "number",
                                "description": "The individual out-of-pocket limit for out-of-network services"
                            },
                            "out_of_network_family_oop_limit": {
                                "type": "number",
                                "description": "The family out-of-pocket limit for out-of-network services"
                            },
                            "plan_name": {
                                "type": "string",
                                "description": "The full name of the health insurance plan"
                            },
                            "plan_year": {
                                "type": "integer",
                                "description": "The year for which the plan is effective"
                            },
                            "plan_status": {
                                "type": "string",
                                "description": "The current status of the plan (e.g., active, inactive)"
                            },
                            "plan_type": {
                                "type": "string",
                                "description": "The type of plan (e.g., HMO, PPO, EPO)"
                            },
                            "plan_design": {
                                "type": "string",
                                "description": "The design type of the plan, such as 'Standard', 'High Deductible', etc."
                            },
                            "metal_level": {
                                "type": "string",
                                "description": "The metal level of the plan (e.g., Bronze, Silver, Gold, Platinum)"
                            },
                            "coverage_type": {
                                "type": "string",
                                "description": "The type of coverage provided (e.g., individual, family)"
                            },
                            "funding_arrangement": {
                                "type": "string",
                                "description": "The funding arrangement for the plan (e.g., fully insured, self-funded)"
                            },
                            "group_size": {
                                "type": "integer",
                                "description": "The size of the group for which the plan is designed"
                            },
                            "network_type": {
                                "type": "string",
                                "description": "The type of provider network used by the plan"
                            },
                            "effective_date": {
                                "type": "string",
                                "description": "The date when the plan becomes effective. formatted to be loaded into a PostgreSQL Database Column with Type Date"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "The date when the plan coverage ends.  formatted to be loaded into a PostgreSQL Database Column with Type Date."
                            },
                            "employer_contribution": {
                                "type": "number",
                                "description": "The percentage or amount of employer contribution to the premium"
                            },
                            "actuarial_value": {
                                "type": "number",
                                "description": "The actuarial value of the plan"
                            },
                            "distribution_channels": {
                                "type": "string",
                                "description": "The channels through which the plan is distributed"
                            },
                            "provider_network_link": {
                                "type": "string",
                                "description": "The URL to access the provider network information"
                            },
                            "provider_network_phone": {
                                "type": "string",
                                "description": "The phone number to contact for provider network information"
                            },
                            "plan_marketing_name": {
                                "type": "string",
                                "description": "The marketing name used for the plan"
                            },
                            "market_segment": {
                                "type": "string",
                                "description": "The market segment for which the plan is designed"
                            },
                            "is_hsa_eligible": {
                                "type": "boolean",
                                "description": "Whether the plan is eligible for a Health Savings Account (HSA)"
                            },
                            "deductible_combined_separate": {
                                "type": "string",
                                "description": "Whether the deductible is combined or separate for different services"
                            },
                            "specialist_referral_required": {
                                "type": "boolean",
                                "description": "Whether a referral is required to see a specialist"
                            },
                            "grandfathered_plan": {
                                "type": "boolean",
                                "description": "Whether the plan is a grandfathered plan under the Affordable Care Act"
                            }
                        },
                        "required": [
                            "in_network_individual_deductible", "in_network_family_deductible",
                            "out_of_network_individual_deductible", "out_of_network_family_deductible",
                            "in_network_individual_oop_limit", "in_network_family_oop_limit",
                            "out_of_network_individual_oop_limit", "out_of_network_family_oop_limit",
                            "plan_name", "plan_year", "plan_status", "plan_type", "plan_design",
                            "metal_level", "coverage_type", "funding_arrangement", "group_size",
                            "network_type", "effective_date", "end_date", "employer_contribution",
                            "actuarial_value", "distribution_channels", "provider_network_link",
                            "provider_network_phone", "plan_marketing_name", "market_segment",
                            "is_hsa_eligible", "deductible_combined_separate",
                            "specialist_referral_required", "grandfathered_plan"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        }

        # Send request to ChatGPT API
        response = client.chat.completions.create(**payload)

        # Extract the details from the response
        result = json.loads(response.choices[0].message.content)

        # Update the product in the database
        for key, value in result.items():
            if hasattr(product, key):
                setattr(product, key, value)

        session.commit()

        print(f"Successfully updated details for product ID {product_id}")
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()
        return None

    finally:
        session.close()

# Example usage:
# result = extract_product_details(1)  # Where 1 is the ID of the product you want to update