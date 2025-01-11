import psycopg2
from psycopg2 import OperationalError

# Database connection parameters
db_params = {
    'dbname': 'IPTR',  # Database name
    'user': 'postgres',  # Username
    'password': 'Steels$Paints',  # Password
    'host': '10.10.50.59',  # Host
    'port': '5432'  # Port
}

def list_tables(schema_name, subunit=None):
    try:
        # Establish the connection using context manager
        with psycopg2.connect(**db_params) as conn:
            print(f"Connected to database {db_params['dbname']}")

            # Create a cursor object
            with conn.cursor() as cursor:
                # Base query to fetch tables
                query = f"""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = '{schema_name}'
                    AND table_type = 'BASE TABLE'
                """

                # Add the subunit filter if subunit is provided
                if subunit:
                    # Convert schema and subunit to uppercase for proper matching
                    prefix = f"{schema_name.split('_')[1].upper()}_"  # Extracts "HSM2_" for 'db1_phsm2', "SMS2_" for 'db1_psms2'
                    query += f" AND table_name LIKE '{prefix}{subunit.upper()}%'"

                query += " ORDER BY table_name;"

                # Execute the query
                cursor.execute(query)

                # Fetch all results
                tables = cursor.fetchall()

                # Return the table names as a list
                return [table[0] for table in tables]

    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
