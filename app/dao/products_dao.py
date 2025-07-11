from server import GetDBConnection


class ProductsDAO:
    def __init__(self):
        self.connection = GetDBConnection()
        self.cursor = self.connection.cursor()
        print("> (Products) Connection to PostreSQL was successfull...")

    def GetProducts(self):
        """
        Fetches all products from the database.
        Returns a list of dictionaries, each representing a product.
        """
        try:
            self.cursor.execute("SELECT * FROM products;")
            rows = self.cursor.fetchall()
            # Get column names from the cursor description
            columns = [desc[0] for desc in self.cursor.description]
            # Convert rows to a list of dictionaries
            products = [dict(zip(columns, row)) for row in rows]
            return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return None

    def GetProductById(self, product_id):
        """
        Fetches a product by its ID from the database.
        Returns a dictionary representing the product.
        """
        try:
            self.cursor.execute("SELECT * FROM products WHERE id = %s;", (product_id))
            row = self.cursor.fetchone()[0]
            columns = [desc[0] for desc in self.cursor.description]
            product = dict(zip(columns, row)) if row else None
            return product
        except Exception as e:
            print(f"Error fetching product by ID: {e}")
            return None

    def CreateProduct(self, product_name: str, unit: str, price) -> int | None:
        try:
            if not isinstance(product_name, str):
                print(
                    f"Error: product_name must be a string, but got {type(product_name)}"
                )
                raise TypeError
                return None

            self.cursor.execute(
                "SELECT product_id FROM products WHERE product_name = %s;",
                (product_name,),
            )
            duplicate = self.cursor.fetchone()[0]

            if duplicate:
                print(
                    f"Error: Product with name '{product_name}' already exists with ID {duplicate}."
                )
                return None

            self.cursor.execute(
                "INSERT INTO products (product_name, unit, price) VALUES (%s, %s, %s) RETURNING product_id;",
                (product_name, unit, price),
            )
            product_id = self.cursor.fetchone()[0]

            if product_id:
                self.connection.commit()
                return product_id
            else:
                self.connection.rollback()
                print("Error: Failed to retrieve product_id after insert.")
                return None
        except TypeError as e:
            print(f"Error creating product (TypeError): {e}")
            print(
                f"Debug Info: product_name type: {type(product_name)}, value: '{product_name}'"
            )
            print(f"Debug Info: unit type: {type(unit)}, value: '{unit}'")
            print(f"Debug Info: price type: {type(price)}, value: '{price}'")
            self.connection.rollback()
            return None
        except Exception as e:
            print(f"Error creating product (General Exception): {e}")
            self.connection.rollback()
            return None

    def UpdateProduct(
        self, product_id: int, category_id: int, unit: str, price: float
    ) -> int | None:
        try:
            self.cursor.execute(
                "UPDATE products SET category_id=%s, unit=%s, price=%s WHERE product_id=%s RETURNING product_id;",
                (category_id, unit, price, product_id),
            )
            prod_id = self.cursor.fetchone()[0]
            if prod_id:
                self.connection.commit()
                return prod_id
            else:
                self.connection.rollback()
                print(f"Info: Product with ID {product_id} not found for update.")
                return None
        except Exception as e:
            print(f"Error updating product: {e}")
            self.connection.rollback()
            return None

    def DeleteProduct(self, product_id: int) -> int | None:
        try:
            self.cursor.execute(
                "DELETE FROM products WHERE product_id=%s RETURNING product_id;",
                (product_id,),
            )
            # Based on the error "'int' object does not support indexing" on a line
            # like `var = fetchone()[0]`, we assume fetchone() might be returning
            # an integer directly when a row is found with RETURNING, or None otherwise.

            deleted_id = self.cursor.fetchone()
            if deleted_id is not None:
                self.connection.commit()
                return deleted_id
            else:
                self.connection.rollback()
                print(f"Info: Product with ID {product_id} not found for deletion.")
                return None
        except Exception as e:
            print(f"Error deleting product with ID {product_id}: {e}")
            self.connection.rollback()
            return None
