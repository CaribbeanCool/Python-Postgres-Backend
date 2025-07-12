from server import GetDBConnection
from typing import List, Dict, Any, Optional


class CategoriesDAO:
    @staticmethod
    def GetCategories() -> List[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM categories")
                results = cursor.fetchall()

                categories = []
                for result in results:
                    categories.append(
                        {
                            "category_id": result[0],
                            "category_name": result[1],
                            "description": result[2],
                        }
                    )
                return categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetCategoryByID(category_id: int) -> Optional[Dict[str, Any]]:
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM categories WHERE category_id = %s", (category_id,)
                )
                result = cursor.fetchone()

                if result:
                    return {
                        "category_id": result[0],
                        "category_name": result[1],
                        "description": result[2],
                    }
                return None
        except Exception as e:
            print(f"Error fetching category: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateCategory(category_name: str, description: str) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO categories (category_name, description) VALUES (%s, %s)",
                    (category_name, description),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error creating category: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def UpdateCategory(category_id: int, category_name: str, description: str) -> bool:
        conn = GetDBConnection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE categories SET category_name = %s, description = %s WHERE category_id = %s",
                    (category_name, description, category_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating category: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            conn.close()
