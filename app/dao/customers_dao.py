from app.server import GetDBConnection

class CustomersDAO:
    def __init__(self):
        """
        Initialize the DAO with a database connection and cursor.
        """
        self.connection = GetDBConnection()
        self.cursor = self.connection.cursor()
        print("> (Customers) Connection to PostreSQL was successfull...")

    def GetCustomers(self):
        """
        Fetches all customers from the database.
        """
        try:
            self.cursor.execute("SELECT * FROM customers")
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            customers = [dict(zip(columns, row)) for row in rows]
            return customers
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return None

    def GetCustomerById(self, customer_id):
        """
        Fetches a customer by ID from the database.
        This method retrieves a single customer record based on the provided customer ID.

        Args:
            customer_id (int): The ID of the customer to fetch.

        Returns:
            dict: A dictionary representing the customer record, or None if not found.
        """
        try:
            self.cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            row = self.cursor.fetchone()
            columns = [desc[0] for desc in self.cursor.description]
            customer = dict(zip(columns, row)) if row else None
            return customer
        except Exception as e:
            print(f"Error fetching customer by ID: {e}")
            return None

    def CreateCustomer(self, name:str, email:str):
        """
        Creates a new customer in the database.
        This method inserts a new customer into the customers table and returns the new customer's ID.

        Args:
            name (str): The name of the customer.
            email (str): The email of the customer.

        Returns:
            int: The ID of the newly created customer.
        """
        try:
            self.cursor.execute(
                "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING customer_id",
                (name, email)
            )
            customer_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return customer_id
        except Exception as e:
            print(f"Error creating customer: {e}")
            return None