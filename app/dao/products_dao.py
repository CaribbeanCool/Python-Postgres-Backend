from server import GetDBConnection
from typing import List, Dict, Any, Optional


class ProductsDAO:
    @staticmethod
    def GetProducts() -> List[Dict[str, Any]]:
        """
        Fetches all products from the database.
        Returns a list of dictionaries, each representing a product.
        """
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                products = []
                for result in results:
                    products.append(dict(zip(columns, result)))
                return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetProductById(product_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetches a product by its ID from the database.
        Returns a dictionary representing the product.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM products WHERE product_id = %s", (product_id,)
                )
                result = cursor.fetchone()

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
        except Exception as e:
            print(f"Error fetching product by ID: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateProduct(product_name: str, unit: str, price: float) -> Optional[int]:
        """
        Creates a new product in the database.
        Returns the ID of the newly created product.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                # Check for duplicate product name
                cursor.execute(
                    "SELECT product_id FROM products WHERE product_name = %s",
                    (product_name,),
                )
                duplicate = cursor.fetchone()

                if duplicate:
                    print(
                        f"Error: Product with name '{product_name}' already exists with ID {duplicate[0]}."
                    )
                    return None

                # Insert new product
                cursor.execute(
                    "INSERT INTO products (product_name, unit, price) VALUES (%s, %s, %s) RETURNING product_id",
                    (product_name, unit, price),
                )
                product_id = cursor.fetchone()[0]
                conn.commit()
                return product_id
        except Exception as e:
            print(f"Error creating product: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def UpdateProduct(
        product_id: int, category_id: int, unit: str, price: float
    ) -> Optional[int]:
        """
        Updates an existing product in the database.
        Returns the ID of the updated product.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE products SET category_id=%s, unit=%s, price=%s WHERE product_id=%s RETURNING product_id",
                    (category_id, unit, price, product_id),
                )
                result = cursor.fetchone()

                if result:
                    conn.commit()
                    return result[0]
                else:
                    print(f"Info: Product with ID {product_id} not found for update.")
                    return None
        except Exception as e:
            print(f"Error updating product: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def DeleteProduct(product_id: int) -> Optional[int]:
        """
        Deletes a product from the database.
        Returns the ID of the deleted product.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM products WHERE product_id=%s RETURNING product_id",
                    (product_id,),
                )
                result = cursor.fetchone()

                if result:
                    conn.commit()
                    return result[0]
                else:
                    print(f"Info: Product with ID {product_id} not found for deletion.")
                    return None
        except Exception as e:
            print(f"Error deleting product with ID {product_id}: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()
