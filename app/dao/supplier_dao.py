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
                columns = [desc[0] for desc in cursor.description]

                suppliers = []
                for result in results:
                    suppliers.append(dict(zip(columns, result)))
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
                    "SELECT * FROM supply_chain.supplier WHERE sid = %s",
                    (supplier_id,),
                )
                result = cursor.fetchone()

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                else:
                    return None
        except Exception as e:
            print(f"Error fetching supplier: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateSupplier(
        supplier_name: str, supplier_city: str, supplier_phone: str
    ) -> Optional[int]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                # check for duplicate supplier name
                cursor.execute(
                    "SELECT * FROM supply_chain.supplier WHERE sname = %s",
                    (supplier_name,),
                )
                if cursor.fetchone():
                    print("Supplier with this name already exists.")
                    return None

                cursor.execute(
                    "INSERT INTO supply_chain.supplier (sname, scity, sphone) VALUES (%s, %s, %s) RETURNING sid",
                    (supplier_name, supplier_city, supplier_phone),
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
                    "UPDATE supply_chain.supplier SET supplier_name = %s WHERE sid = %s",
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
                    "DELETE FROM supply_chain.supplier WHERE sid = %s",
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

    @staticmethod
    def GetSupplierWithPartsAbovePrice(price: float) -> List[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                query = """
                select distinct sid, sname, pmaterial, pprice
                from supplier s
                natural inner join supplies su
                natural inner join part p
                where p.pprice > (%s);
                """
                cursor.execute(query, (price,))
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                suppliers = []
                for result in results:
                    suppliers.append(dict(zip(columns, result)))
                return suppliers
        except Exception as e:
            print(f"Error fetching suppliers with parts above price: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetSuppliersByCityandMaterial(city: str, material: str) -> List[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                query = """
                select sid, sname, scity, pmaterial
                from supplier s
                natural inner join supplies su
                natural inner join part p
                where s.scity = %s
                and p.pmaterial = %s
                order by s.sid;
                """
                cursor.execute(query, (city, material))
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                suppliers = []
                for result in results:
                    suppliers.append(dict(zip(columns, result)))
                return suppliers
        except Exception as e:
            print(f"Error fetching suppliers by city and material: {e}")
            return []
        finally:
            conn.close()
