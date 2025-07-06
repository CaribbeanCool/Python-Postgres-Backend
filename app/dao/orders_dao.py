from app.server import GetDBConnection

class OrdersDAO:
    """
    Orders Data Access Object (DAO) class for interacting with the database.
    This class provides methods to fetch orders and order details from the database.
    It uses a singleton pattern to ensure that only one instance of the database connection is used.
    """

    def __init__(self):
        """
        Initialize the DAO with a database connection and cursor.
        """
        self.connection = GetDBConnection()
        self.cursor = self.connection.cursor()
        print("> (Orders) Connection to PostreSQL was successfull...")

    def GetOrders(self):
        """
        Fetches all orders from the database.
        Returns a list of dictionaries, each representing an order.
        """
        try:
            self.cursor.execute("SELECT * FROM orders;")
            rows = self.cursor.fetchall()
            # Get column names from the cursor description
            columns = [desc[0] for desc in self.cursor.description]
            # Convert rows to a list of dictionaries
            orders = [dict(zip(columns, row)) for row in rows]
            return orders
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return None

    def GetOrderById(self, order_id):
        """
        Fetches an order by its ID from the database.
        Returns a dictionary representing the order.
        """
        try:
            self.cursor.execute("SELECT * FROM orders WHERE order_id = %s;", (order_id,))
            row = self.cursor.fetchone()
            columns = [desc[0] for desc in self.cursor.description]
            order = dict(zip(columns, row)) if row else None
            return order
        except Exception as e:
            print(f"Error fetching order by ID: {e}")
            return None

    def CreateOrder(self, customer_id, order_date):
        """
        Creates a new order in the database.
        Returns the ID of the newly created order.
        """
        try:
            self.cursor.execute("INSERT INTO orders (customer_id, order_date) VALUES (%s, %s) RETURNING id;", (customer_id, order_date))
            order_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return order_id
        except Exception as e:
            print(f"Error creating order: {e}")
            self.connection.rollback()
            return None