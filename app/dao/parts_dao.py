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
                cursor.execute("SELECT * FROM supply_chain.parts")
                results = cursor.fetchall()

                parts = []
                for result in results:
                    parts.append(
                        {
                            "part_id": result[0],
                            "part_name": result[1],
                        }
                    )
                return parts
        except Exception as e:
            print(f"Error fetching parts: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetPartById(part_id: int) -> Optional[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM supply_chain.parts WHERE part_id = %s", (part_id,)
                )
                result = cursor.fetchone()

                if result:
                    return {
                        "part_id": result[0],
                        "part_name": result[1],
                    }
                return None
        except Exception as e:
            print(f"Error fetching part: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreatePart(part_name: str) -> Optional[int]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO supply_chain.parts (part_name) VALUES (%s) RETURNING part_id",
                    (part_name,),
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
    def UpdatePart(part_id: int, part_name: str) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE supply_chain.parts SET part_name = %s WHERE part_id = %s",
                    (part_name, part_id),
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
    def DeletePart(part_id: int) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM supply_chain.parts WHERE part_id = %s", (part_id,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting part: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()
