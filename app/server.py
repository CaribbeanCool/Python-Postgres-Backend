import psycopg2
from psycopg2 import OperationalError, Error
from dotenv import load_dotenv
import os

load_dotenv()

def GetDBConnection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    If the connection fails, it prints the error and returns None.
    """
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            dbname=os.getenv('DBNAME'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            port=os.getenv('PORT')
        )
        return connection
    except OperationalError as error:
        print("> Error: Unable to connect to PostgreSQL. Is the Docker container running?")
        print("> Detailed error:\n", error)
        return None
    except (Exception, Error) as error:
        print("> Error while connecting to PostgreSQL:", error)
        return None