import psycopg2
from psycopg2.extensions import connection
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

if os.getenv("APP_ENV") == "dev":
    DBNAME = os.getenv("DBNAME_TEST", "supply_chain")
    print("\n***\nUsing supply_chain database...\n***\n")
else:
    DBNAME = os.getenv("DBNAME")
    print("\n***\nUsing default database...\n***\n")


def GetDBConnection() -> Optional[connection]:
    """
    Establishes and returns a connection to the PostgreSQL database.
    If the connection fails, it prints the error and returns None.
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DBNAME,
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
        )
        return conn
    except Exception as error:
        print("> Error while connecting to PostgreSQL:", error)
        return None
