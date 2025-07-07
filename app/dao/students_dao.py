from app.server import GetDBConnection


class StudentDAO:
    def __init__(self):
        self.connection = GetDBConnection()
        self.cursor = self.connection.cursor()
        print("> (Students) Connection to PostreSQL was successfull...")

    def GetStudents(self):
        """
        Fetches all students from the database.
        Returns a list of dictionaries, each representing a product.
        """
        try:
            self.cursor.execute("SELECT * FROM students;")
            rows = self.cursor.fetchall()
            # Get column names from the cursor description
            columns = [desc[0] for desc in self.cursor.description]
            # Convert rows to a list of dictionaries
            students = [dict(zip(columns, row)) for row in rows]
            return students
        except Exception as e:
            print(f"Error fetching products: {e}")
            return None

    def GetStudentById(self, student_id):
        """
        Fetches a student by its ID from the database.
        Returns a dictionary representing the product.
        """
        try:
            self.cursor.execute("SELECT * FROM students WHERE id = %s;", (student_id))
            row = self.cursor.fetchone()[0]
            columns = [desc[0] for desc in self.cursor.description]
            student = dict(zip(columns, row)) if row else None
            return student
        except Exception as e:
            print(f"Error fetching product by ID: {e}")
            return None

    def CreateStudent(
        self, first_name: str, last_name: str, email: str, date_of_birth
    ) -> int | None:
        # date_of_birth can be a datetime.date object or 'YYYY-MM-DD' string
        try:
            # Optional: Add a check for duplicate students if necessary, e.g., by email
            # self.cursor.execute("SELECT student_id FROM students WHERE email = %s;", (email,))
            # existing_student = self.cursor.fetchone()
            # if existing_student:
            #     print(f"Error: Student with email '{email}' already exists with ID {existing_student[0]}.")
            #     return None

            self.cursor.execute(
                """
                INSERT INTO students (first_name, last_name, email, date_of_birth) 
                VALUES (%s, %s, %s, %s) 
                RETURNING student_id; 
                """,
                (first_name, last_name, email, date_of_birth),
            )
            student_id = self.cursor.fetchone()[0]

            if student_id:
                self.connection.commit()
                return student_id
            else:
                self.connection.rollback()
                print("Error: Failed to retrieve student_id after insert.")
                return None
        except TypeError as e:
            # Catch potential type errors, e.g. if date_of_birth is not in a compatible format
            print(f"Error creating student (TypeError): {e}")
            print(
                f"Debug Info: first_name: {first_name}, last_name: {last_name}, email: {email}, date_of_birth: {date_of_birth} (type: {type(date_of_birth)})"
            )
            self.connection.rollback()
            return None
        except Exception as e:
            print(f"Error creating student (General Exception): {e}")
            self.connection.rollback()
            return None

    # def UpdateStudent(self, product_id: int, category_id:int, unit:str, price:float) -> int | None:
    #     try:
    #         self.cursor.execute(
    #             "UPDATE products SET category_id=%s, unit=%s, price=%s WHERE product_id=%s RETURNING product_id;",
    #             (category_id, unit, price, product_id)
    #         )
    #         prod_id = self.cursor.fetchone()[0]
    #         if prod_id:
    #             self.connection.commit()
    #             return prod_id
    #         else:
    #             self.connection.rollback()
    #             print(f"Info: Product with ID {product_id} not found for update.")
    #             return None
    #     except Exception as e:
    #         print(f"Error updating product: {e}")
    #         self.connection.rollback()
    #         return None

    # def DeleteStudent(self, product_id: int) -> int | None:
    #     try:
    #         self.cursor.execute(
    #             "DELETE FROM products WHERE product_id=%s RETURNING product_id;",
    #             (product_id,)
    #         )
    #         # Based on the error "'int' object does not support indexing" on a line
    #         # like `var = fetchone()[0]`, we assume fetchone() might be returning
    #         # an integer directly when a row is found with RETURNING, or None otherwise.

    #         deleted_id = self.cursor.fetchone()
    #         if deleted_id is not None:
    #             self.connection.commit()
    #             return deleted_id
    #         else:
    #             self.connection.rollback()
    #             print(f"Info: Product with ID {product_id} not found for deletion.")
    #             return None
    #     except Exception as e:
    #         print(f"Error deleting product with ID {product_id}: {e}")
    #         self.connection.rollback()
    #         return None
