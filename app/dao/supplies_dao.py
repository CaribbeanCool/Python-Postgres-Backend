from server import GetDBConnection
from typing import List, Dict, Any, Optional


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

                supplies = []
                for result in results:
                    supplies.append(
                        {
                            "supply_id": result[0],
                            "supplier_id": result[1],
                            "part_id": result[2],
                            "quantity": result[3],
                        }
                    )
                return supplies
        except Exception as e:
            print(f"Error fetching supplies: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetSupplyById(supply_id: int) -> Optional[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM supply_chain.supplies WHERE supply_id = %s",
                    (supply_id,),
                )
                result = cursor.fetchone()

                if result:
                    return {
                        "supply_id": result[0],
                        "supplier_id": result[1],
                        "part_id": result[2],
                        "quantity": result[3],
                    }
                return None
        except Exception as e:
            print(f"Error fetching supply: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateSupply(supplier_id: int, part_id: int, quantity: int) -> Optional[int]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO supply_chain.supplies (supplier_id, part_id, quantity) VALUES (%s, %s, %s) RETURNING supply_id",
                    (supplier_id, part_id, quantity),
                )
                result = cursor.fetchone()
                conn.commit()
                return result[0] if result else None
        except Exception as e:
            print(f"Error creating supply: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def UpdateSupply(supply_id: int, quantity: int) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE supply_chain.supplies SET quantity = %s WHERE supply_id = %s",
                    (quantity, supply_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating supply: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def DeleteSupply(supply_id: int) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM supply_chain.supplies WHERE supply_id = %s",
                    (supply_id,),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting supply: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()
