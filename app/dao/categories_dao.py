from app.server import GetDBConnection

class CategoriesDAO:
    """
    Categories Data Access Object (DAO) class for interacting with the database.
    This class provides methods to fetch categories and category details from the database.
    It uses a single pattern to ensure that only one instance of the database connection is used.
    """

    def __init__(self):
        """
        Initialize the DAO with a database connection and cursor.
        """
        self.connection = GetDBConnection()
        self.cursor = self.connection.cursor()
        print("> (Categories) Connection to PostreSQL was successfull...")

    def GetCategories(self):
        """
        Fetches all categories from the database.
        Returns a list of dictionaries, each representing a category.
        """
        try:
            self.cursor.execute("SELECT * FROM categories;")
            # Fetch all rows from the executed query
            rows = self.cursor.fetchall()
            # Get column names from the cursor description
            columns = [desc[0] for desc in self.cursor.description]
            # Convert rows to a list of dictionaries
            categories = [dict(zip(columns, row)) for row in rows]
            return categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return None

    def GetCategoryById(self, category_id:int):
        """
        Fetches a category by its ID from the database.
        Returns a dictionary representing the category.
        """
        try:
            self.cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
            row = self.cursor.fetchone()
            columns = [desc[0] for desc in self.cursor.description]
            category = dict(zip(columns, row)) if row else None
            return category
        except Exception as e:
            print(f"Error fetching category by ID: {e}")
            return None

    def CreateCategory(self, category_name:str):
        """
        Creates a new category in the database.
        Returns the ID of the newly created category.
        """
        try:
            self.cursor.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id;", (category_name,))
            category_id = self.cursor.fetchone()[0]
            self.connection.commit()  # Commit the transaction
            return category_id
        except Exception as e:
            print(f"Error creating category: {e}")
            self.connection.rollback()

    def UpdateCategory(self, description:str, category_id:int):
        """
        Updates an existing category in the database.
        Returns True if the update was successful, False otherwise.
        """
        try:
            self.cursor.execute("UPDATE categories SET description = %s WHERE category_id = %s;", (description, category_id))
            self.connection.commit()  # Commit the transaction
            return category_id
        except Exception as e:
            print(f"Error updating category: {e}")
            self.connection.rollback()
            return None