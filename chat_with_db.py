import os
import openai
from langchain_openai import ChatOpenAI  # Updated import for ChatOpenAI
from sqlalchemy import create_engine, text, inspect
import argparse
from tabulate import tabulate  # For pretty-printing the results
import re

# Fetch database credentials and OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PGDATABASE = os.getenv("PGDATABASE")
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT", "5432")  # Default to PostgreSQL's default port if not set
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")

# Set up the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Create the PostgreSQL connection string (DATABASE_URL)
DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"

# Define the database connection
engine = create_engine(DATABASE_URL)

# Set up the LangChain LLM
llm = ChatOpenAI(
    model_name="gpt-4o-mini",  # Correct parameter for the model
    temperature=0.7  # Adjust the temperature as needed
)

def get_db_schema():
    """
    Function to retrieve the columns from the 'product' table in the database.
    """
    inspector = inspect(engine)
    schema_info = {}

    # Check if the 'product' table exists
    if 'product' in inspector.get_table_names():
        # Get columns for the 'product' table
        columns = inspector.get_columns('product')
        column_names = [column['name'] for column in columns]
        schema_info['product'] = column_names
    else:
        print("Error: The 'product' table does not exist in the database.")
        return None

    return schema_info

def generate_prompt(question: str, schema_info: dict):
    """
    Generate a prompt with schema information to guide the LLM.
    """
    schema_str = "\n".join([f"Table: {table}, Columns: {', '.join(columns)}" for table, columns in schema_info.items()])
    prompt = f"""
    You are an assistant with access to a PostgreSQL database. The database schema is as follows:
    {schema_str}

    Based on this schema, write a SQL query to answer the following question: '{question}'.
    """
    return prompt

def query_database(query: str):
    """
    Function to query the database and return results.
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return [row for row in result]

def format_output(results):
    """
    Format the output to display it in a readable manner.
    """
    if not results:
        print("No results found.")
        return

    # Convert results to a list of tuples for easy display
    results_list = [list(row) for row in results]

    if results_list:
        # Print a debug statement with the first few rows for clarity
        print(f"Debug: First row from results: {results_list[0]}")

    # Truncate long columns (like URLs or long descriptions)
    for row in results_list:
        for idx, value in enumerate(row):
            if isinstance(value, str) and len(value) > 50:  # If the text is too long, truncate it
                row[idx] = value[:50] + '...'  # Truncate long text and add ellipsis

    # Display the results in a pretty table
    print(tabulate(results_list, headers="keys", tablefmt="grid"))

def extract_sql_query(response_content):
    """
    Extract the SQL query from the response content.
    """
    # Use a regex to extract content between the SQL block (` ```sql ` and ` ``` `)
    match = re.search(r'```sql(.*?)```', response_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def chat_with_data(question: str):
    """
    Function that uses LangChain to chat with the database.
    It generates SQL queries from natural language questions, considering the schema.
    """
    # Get the database schema
    schema_info = get_db_schema()

    # Generate the prompt using the schema information
    prompt = generate_prompt(question, schema_info)

    # Generate the SQL query using the language model
    response = llm.invoke(prompt)  # Invoke the LLM to get a response

    # Access the content from the AIMessage object
    sql_query = extract_sql_query(response.content)

    if not sql_query:
        print("Error: No valid SQL query found in the response.")
        return

    # Print the generated SQL query for debugging
    print(f"Generated SQL Query:\n{sql_query}\n")

    try:
        # Query the database using the generated SQL query
        results = query_database(sql_query)
        if results:
            format_output(results)  # Format and display the output
        else:
            print("No results were returned from the query.")
    except Exception as e:
        print(f"Error querying the database: {e}")

def main():
    """
    Main function to handle command-line input and chat with the database.
    """
    parser = argparse.ArgumentParser(description="Chat with your database using LangChain.")
    parser.add_argument('question', type=str, help="The question to ask the database.")
    args = parser.parse_args()

    chat_with_data(args.question)

if __name__ == "__main__":
    main()
