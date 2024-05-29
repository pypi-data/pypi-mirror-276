import psycopg2
from app.general_tools.logger import logger
import pandas as pd
from sqlalchemy import text
from psycopg2 import sql
import csv



'''
Connect to Postgres Database
'''
def connect_to_db():
    try:
        logger.info("Trying to connect to Postgres database...")
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="htb",
            user="gpanagou",
            password="my_secret_password"
        )
        return connection
    except psycopg2.DatabaseError as error:
        logger.error(f"Error while connecting to PostgreSQL: {error}")
        return None

'''
Function that inserts data to Postgres database
'''
 
def insert_csv_data_to_postgres(csv_table_mapping):
    try:
        # Connect to the PostgreSQL database
        conn = connect_to_db()

        # Create a cursor object
        cur = conn.cursor()

        # Iterate over each (csv_file, table_name) pair
        for csv_file, table_name in csv_table_mapping:
            # Open the CSV file
            with open(csv_file, 'r', encoding='utf-8') as f:
                # Create a CSV reader object
                reader = csv.reader(f)
                # Skip the header row
                next(reader)
                # Initialize id counter if the table name is 'machine_ratings'
                id_counter = 1 if table_name == 'machine_ratings' else None
                # Iterate over each row in the CSV file
                for row in reader:
                    # Check if the table name is 'machine_ratings'
                    if table_name == 'machine_ratings':
                        # Add an incremental ID in front of each row
                        row.insert(0, id_counter)
                        # Increment the id counter
                        id_counter += 1
                    # Construct the SQL query to insert a row
                    data = [None if val == '' else val for val in row]
                    placeholders = ', '.join(['%s'] * len(data))
                    insert_query = sql.SQL("INSERT INTO {} VALUES ({})").format(
                        sql.Identifier(table_name),
                        sql.SQL(placeholders)
                    )
                    # Execute the query
                    cur.execute(insert_query, data)

        # Commit the transaction
        conn.commit()

        logger.info("Data inserted successfully!")

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error while inserting data to PostgreSQL: {error}")

    finally:
        # Close the cursor and connection
        if conn:
            cur.close()
            conn.close()

# '''
# Function that fetches data
# '''

def fetch_data(session):
    query = """
        SELECT *
FROM (
    WITH temp AS (
        SELECT co.*, mr.*, mrr.*, 
            ROW_NUMBER() OVER (PARTITION BY co.content_name ORDER BY co.content_name) AS row_num
        FROM 
            public.content_owns co 
        LEFT JOIN public.machines mr ON co.content_id = mr.content_id
        LEFT JOIN (
            SELECT DISTINCT ON (machine_name) *
            FROM public.machine_ratings
        ) AS mrr ON mr.machine_name = mrr.machine_name
    )
    SELECT *
    FROM temp
) AS subquery;
    """
    
    try:
        # Execute the query
        result = session.execute(text(query))
        rows = result.fetchall()
        
        # Get column names
        colnames = result.keys()
        df = pd.DataFrame(rows, columns=colnames)
        
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        session.close()