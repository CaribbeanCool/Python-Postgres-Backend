from server import GetDBConnection
from typing import List, Dict, Any, Optional


class OrdersDAO:
    """
    Orders Data Access Object (DAO) class for interacting with the database.
    This class provides methods to fetch orders and order details from the database.
    """

    @staticmethod
    def GetOrders() -> List[Dict[str, Any]]:
        """
        Fetches all orders from the database.
        Returns a list of dictionaries, each representing an order.
        """
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM orders")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                orders = []
                for result in results:
                    orders.append(dict(zip(columns, result)))
                return orders
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetOrderById(order_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetches an order by its ID from the database.
        Returns a dictionary representing the order.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
                result = cursor.fetchone()

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
        except Exception as e:
            print(f"Error fetching order by ID: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateOrder(customer_id: int, order_date: str) -> Optional[int]:
        """
        Creates a new order in the database.
        Returns the ID of the newly created order.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO orders (customer_id, order_date) VALUES (%s, %s) RETURNING order_id",
                    (customer_id, order_date),
                )
                order_id = cursor.fetchone()[0]
                conn.commit()
                return order_id
        except Exception as e:
            print(f"Error creating order: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()
