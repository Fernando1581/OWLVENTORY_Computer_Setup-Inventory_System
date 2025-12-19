from models.database import get_connection
from mysql.connector import Error

class EmployeeModel:
    @staticmethod
    def login(emp_id, password):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Employee WHERE employeeID=%s AND password=%s",
                (emp_id, password)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            raise e

    @staticmethod
    def register(fn, mn, ln, password):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Employee (Fn, Mn, Ln, password) VALUES (%s, %s, %s, %s)",
                (fn, mn, ln, password)
            )
            conn.commit()
            employee_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return employee_id
        except Error as e:
            raise e

    @staticmethod
    def save_request(pcNo, emp_id, hardware, reason):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO requests (pcNo, employeeID, hardware, reason) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (pcNo, emp_id, hardware, reason))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            raise e