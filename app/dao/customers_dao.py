from server import GetDBConnection
from typing import List, Dict, Any, Optional


class CustomersDAO:
    @staticmethod
    def GetCustomers() -> List[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM customers")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                customers = []
                for result in results:
                    customers.append(dict(zip(columns, result)))
                return customers
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetCustomerById(customer_id: int) -> Optional[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM customers WHERE customer_id = %s", (customer_id,)
                )
                result = cursor.fetchone()

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
        except Exception as e:
            print(f"Error fetching customer by ID: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateCustomer(name: str, email: str) -> Optional[int]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING customer_id",
                    (name, email),
                )
                customer_id = cursor.fetchone()[0]
                conn.commit()
                return customer_id
        except Exception as e:
            print(f"Error creating customer: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()
