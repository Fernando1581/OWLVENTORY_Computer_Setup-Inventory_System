from models.database import get_connection
from mysql.connector import Error

class EmployeeModel:
    @staticmethod
    def login(emp_id, hashed_password):
        """
        Checks if employee exists with this ID and Hashed Password.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM employee WHERE employeeID=%s AND password=%s",
                (emp_id, hashed_password)
            )
            result = cursor.fetchone()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def register(fn, mn, ln, hashed_password):
        """
        Creates a new employee account. Returns the new EmployeeID.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO employee (Fn, Mn, Ln, password) VALUES (%s, %s, %s, %s)",
                (fn, mn, ln, hashed_password)
            )
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def save_request(pcNo, emp_id, hardware, reason):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requests (pcNo, employeeID, hardware, reason) VALUES (%s, %s, %s, %s)",
                           (pcNo, emp_id, hardware, reason))
            conn.commit()
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_all_notifications(emp_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT hardware, status, dateAction FROM requests WHERE employeeID = %s AND status != 'Pending' ORDER BY dateAction DESC",
                (emp_id,))
            result = cursor.fetchall()
            return result
        except Error:
            return []
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def mark_read(emp_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE requests SET is_read = 1 WHERE employeeID = %s AND status != 'Pending'", (emp_id,))
            conn.commit()
        except Error:
            pass
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()