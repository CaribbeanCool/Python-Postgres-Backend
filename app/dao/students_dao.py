from server import GetDBConnection
from typing import List, Dict, Any, Optional


class StudentDAO:
    @staticmethod
    def GetStudents() -> List[Dict[str, Any]]:
        """
        Fetches all students from the database.
        Returns a list of dictionaries, each representing a student.
        """
        conn = GetDBConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM students")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                students = []
                for result in results:
                    students.append(dict(zip(columns, result)))
                return students
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def GetStudentById(student_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetches a student by its ID from the database.
        Returns a dictionary representing the student.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM students WHERE student_id = %s", (student_id,)
                )
                result = cursor.fetchone()

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
        except Exception as e:
            print(f"Error fetching student by ID: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def CreateStudent(
        first_name: str, last_name: str, email: str, date_of_birth: str
    ) -> Optional[int]:
        """
        Creates a new student in the database.
        Returns the ID of the newly created student.
        """
        conn = GetDBConnection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO students (first_name, last_name, email, date_of_birth) VALUES (%s, %s, %s, %s) RETURNING student_id",
                    (first_name, last_name, email, date_of_birth),
                )
                student_id = cursor.fetchone()[0]
                conn.commit()
                return student_id
        except Exception as e:
            print(f"Error creating student: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()
