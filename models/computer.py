from models.database import get_connection
from mysql.connector import Error

class ComputerModel:
    @staticmethod
    def get_pc_by_employee(emp_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT pcNo FROM Computer WHERE assignedEmp=%s",
                (emp_id,)
            )
            pc = cursor.fetchone()
            cursor.close()
            conn.close()
            return pc
        except Error as e:
            raise e

    @staticmethod
    def assign_pc(emp_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT pcNo FROM Computer WHERE assignedEmp IS NULL ORDER BY pcNo LIMIT 1"
            )
            available_pc = cursor.fetchone()
            if available_pc:
                pc_number = available_pc[0]
                cursor.execute(
                    "UPDATE Computer SET assignedEmp=%s, status='Active', dateAssigned=NOW() WHERE pcNo=%s",
                    (emp_id, pc_number)
                )
                conn.commit()
            else:
                pc_number = None
            cursor.close()
            conn.close()
            return pc_number
        except Error as e:
            raise e
