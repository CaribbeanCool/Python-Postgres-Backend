from server import GetDBConnection
from typing import List, Dict, Any, Optional


class SupplierDAO:
    @staticmethod
    def GetSuppliers() -> List[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM supply_chain.supplier")
                results = cursor.fetchall()

                suppliers = []
                for result in results:
                    suppliers.append(
                        {
                            "supplier_id": result[0],
                            "supplier_name": result[1],
                        }
                    )
                return suppliers
        except Exception as e:
            print(f"Error fetching suppliers: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetSupplierById(supplier_id: int) -> Optional[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM supply_chain.supplier WHERE supplier_id = %s",
                    (supplier_id,),
                )
                result = cursor.fetchone()

                if result:
                    return {
                        "supplier_id": result[0],
                        "supplier_name": result[1],
                    }
                return None
        except Exception as e:
            print(f"Error fetching supplier: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateSupplier(supplier_name: str) -> Optional[int]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO supply_chain.supplier (supplier_name) VALUES (%s) RETURNING supplier_id",
                    (supplier_name,),
                )
                result = cursor.fetchone()
                conn.commit()
                return result[0] if result else None
        except Exception as e:
            print(f"Error creating supplier: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def UpdateSupplier(supplier_id: int, supplier_name: str) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE supply_chain.supplier SET supplier_name = %s WHERE supplier_id = %s",
                    (supplier_name, supplier_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating supplier: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def DeleteSupplier(supplier_id: int) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM supply_chain.supplier WHERE supplier_id = %s",
                    (supplier_id,),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting supplier: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()
