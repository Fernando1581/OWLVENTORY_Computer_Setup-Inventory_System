from models.database import get_connection
from mysql.connector import Error


class ComputerModel:
    @staticmethod
    def get_pc_by_employee(emp_id):
        """Finds which PC an employee owns."""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT pcNo FROM computer WHERE assignedEmp=%s", (emp_id,))
            pc = cursor.fetchone()
            return pc
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def assign_pc(emp_id):
        """Finds an empty PC and gives it to the employee."""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Find the first available PC
            cursor.execute("SELECT pcNo FROM computer WHERE assignedEmp IS NULL ORDER BY pcNo LIMIT 1")
            row = cursor.fetchone()

            pc_num = None
            if row:
                pc_num = row[0]
                cursor.execute("UPDATE computer SET assignedEmp=%s, status='Active', dateAssigned=NOW() WHERE pcNo=%s",
                               (emp_id, pc_num))
                conn.commit()

            return pc_num
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()