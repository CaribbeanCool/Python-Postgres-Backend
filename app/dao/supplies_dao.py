from server import GetDBConnection
from typing import List, Dict, Any


class SuppliesDAO:
    """DAO for managing supplies in the supply chain database.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing supplies.
    """

    @staticmethod
    def GetSupplies() -> List[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM supply_chain.supplies")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                supplies = []
                for result in results:
                    supplies.append(dict(zip(columns, result)))
                return supplies
        except Exception as e:
            print(f"Error fetching supplies: {e}")
            return []
        finally:
            conn.close()
