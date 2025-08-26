from server import GetDBConnection
from typing import List, Dict, Any, Optional


class PartsDAO:
    @staticmethod
    def GetParts() -> List[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM supply_chain.part")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                parts = []
                for result in results:
                    parts.append(dict(zip(columns, result)))
                return parts
        except Exception as e:
            print(f"Error fetching parts: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetPartById(pid: int) -> Optional[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM supply_chain.part WHERE pid = %s", (pid,))
                result = cursor.fetchone()

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
        except Exception as e:
            print(f"Error fetching part: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreatePart(
        pname: str, pcolor: str, pmaterial: str, pprice: float, pweight: float
    ) -> Optional[int]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                # find duplicate part names
                cursor.execute(
                    "SELECT * FROM supply_chain.part WHERE pname = %s", (pname,)
                )
                if cursor.fetchone():
                    print("Part with this name already exists.")
                    return None
                cursor.execute(
                    "INSERT INTO supply_chain.part (pname, pcolor, pmaterial, pprice, pweight) VALUES (%s, %s, %s, %s, %s) RETURNING pid",
                    (pname, pcolor, pmaterial, pprice, pweight),
                )
                result = cursor.fetchone()
                conn.commit()
                return result[0] if result else None
        except Exception as e:
            print(f"Error creating part: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def UpdatePart(pid: int, pname: str) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE supply_chain.part SET pname = %s WHERE pid = %s",
                    (pname, pid),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating part: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def DeletePart(pid: int) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM supply_chain.part WHERE pid = %s", (pid,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting part: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()
