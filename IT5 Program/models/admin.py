from models.database import get_connection
from mysql.connector import Error


class AdminModel:
    @staticmethod
    def login(admin_id, password):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT adminID, Fn FROM admin WHERE adminID = %s AND password = %s", (admin_id, password))
            result = cursor.fetchone()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def create_new_computer(admin_id):
        conn = None
        cursor = None
        parts = ["Monitor", "Keyboard & Mouse", "GPU", "Motherboard", "RAM"]

        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            for part in parts:
                cursor.execute("SELECT quantity, hardwareID FROM hardware WHERE hardwareName = %s LIMIT 1", (part,))
                row = cursor.fetchone()
                if not row or row[0] <= 0:
                    raise Exception(f"Stock Error: {part} is unavailable.")

            for part in parts:
                cursor.execute("SELECT hardwareID FROM hardware WHERE hardwareName = %s", (part,))
                hw_id = cursor.fetchone()[0]

                cursor.execute("UPDATE hardware SET quantity = quantity - 1 WHERE hardwareID = %s", (hw_id,))

                cursor.execute(
                    "INSERT INTO stock_logs (hardwareID, quantityChanged, adminID, reason, dateAdded) VALUES (%s, -1, %s, 'New PC Build', NOW())",
                    (hw_id, admin_id)
                )

            cursor.execute("INSERT INTO computer (status, dateAssigned) VALUES ('Available', NULL)")

            conn.commit()
            return True, "Computer created successfully."

        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def update_hardware_stock(name, amount, admin_id, reason):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT hardwareID FROM hardware WHERE hardwareName = %s LIMIT 1", (name,))
            row = cursor.fetchone()

            if row:
                hw_id = row[0]
                cursor.execute("UPDATE hardware SET quantity = quantity + %s WHERE hardwareID = %s", (amount, hw_id))

                cursor.execute(
                    "INSERT INTO stock_logs (hardwareID, quantityChanged, adminID, reason, dateAdded) VALUES (%s, %s, %s, %s, NOW())",
                    (hw_id, amount, admin_id, reason)
                )
                conn.commit()
            else:
                raise Exception(f"Hardware '{name}' not found.")

        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_stock_logs():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT CONCAT(h.hardwareName, ' - ', h.brand), 
                       sl.quantityChanged, 
                       CONCAT(a.Fn, ' ', a.Ln), 
                       sl.reason, 
                       DATE_FORMAT(sl.dateAdded, '%Y-%m-%d %H:%i') 
                FROM stock_logs sl 
                JOIN hardware h ON sl.hardwareID = h.hardwareID 
                JOIN admin a ON sl.adminID = a.adminID 
                ORDER BY sl.dateAdded DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_stock_logs_filtered(start_date, end_date):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            start_str = f"{start_date} 00:00:00"
            end_str = f"{end_date} 23:59:59"

            query = """
                SELECT CONCAT(h.hardwareName, ' - ', h.brand), 
                       sl.quantityChanged, 
                       CONCAT(a.Fn, ' ', a.Ln), 
                       sl.reason, 
                       DATE_FORMAT(sl.dateAdded, '%Y-%m-%d %H:%i') 
                FROM stock_logs sl 
                JOIN hardware h ON sl.hardwareID = h.hardwareID 
                JOIN admin a ON sl.adminID = a.adminID 
                WHERE sl.dateAdded >= %s AND sl.dateAdded <= %s
                ORDER BY sl.dateAdded DESC
            """
            cursor.execute(query, (start_str, end_str))
            result = cursor.fetchall()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_all_computers():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT c.pcNo, IFNULL(CONCAT_WS(' ', e.Fn, e.Mn, e.Ln), 'Unassigned'), c.status FROM computer c LEFT JOIN employee e ON c.assignedEmp = e.employeeID"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_hardware_inventory():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT hardwareName, brand, quantity FROM hardware ORDER BY hardwareID ASC")
            result = cursor.fetchall()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_inventory_snapshot():
        return AdminModel.get_hardware_inventory()

    @staticmethod
    def get_dashboard_kpis():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            stats = {}
            cursor.execute("SELECT COUNT(*) FROM computer WHERE assignedEmp IS NOT NULL")
            stats['active'] = cursor.fetchone()[0]
            cursor.execute("SELECT IFNULL(SUM(quantity), 0) FROM hardware")
            stats['items'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM computer WHERE assignedEmp IS NULL")
            stats['available'] = cursor.fetchone()[0]
            return stats
        except Error:
            return {'active': 0, 'items': 0, 'available': 0}
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_graph_data():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT CONCAT(hardwareName, ' - ', brand), quantity FROM hardware")
            result = cursor.fetchall()
            return result
        except Error:
            return []
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_all_requests():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT r.pcNo, e.employeeID, CONCAT(e.Fn, ' ', e.Ln), r.hardware, r.reason, r.requestID FROM requests r JOIN employee e ON r.employeeID = e.employeeID WHERE r.status = 'Pending'")
            result = cursor.fetchall()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def update_request_status(req_id, status, admin_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE requests SET status = %s, validator = %s WHERE requestID = %s",
                           (status, admin_id, req_id))
            conn.commit()
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_request_history():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Note: r.dateAction is fetched here, which serves as 'Date Started' in the controller
            query = """SELECT r.pcNo, r.employeeID, CONCAT(e.Fn, ' ', e.Ln), r.hardware, r.status, r.dateAction, IFNULL(CONCAT(a.Fn, ' ', a.Ln), r.validator) 
                       FROM requests r JOIN employee e ON r.employeeID = e.employeeID LEFT JOIN admin a ON r.validator = a.adminID WHERE r.status != 'Pending' ORDER BY r.dateAction DESC"""
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def get_all_setups():
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT e.employeeID, CONCAT(e.Fn, ' ', e.Mn, ' ', e.Ln), c.pcNo, c.dateAssigned FROM computer c INNER JOIN employee e ON c.assignedEmp = e.employeeID")
            result = cursor.fetchall()
            return result
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def retire_employee(emp_id, pc_no):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()
            cursor.execute("UPDATE computer SET status='Inactive', assignedEmp=NULL, dateAssigned=NULL WHERE pcNo=%s",
                           (pc_no,))
            cursor.execute("DELETE FROM employee WHERE employeeID=%s", (emp_id,))
            conn.commit()
            return True, "Employee retired successfully."
        except Error as e:
            if conn: conn.rollback()
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def complete_normal_fix(req_id, admin_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE requests SET status = 'Normal Fix', hardware = 'N/A', validator = %s, dateAction = NOW() WHERE requestID = %s"
            cursor.execute(query, (admin_id, req_id))
            conn.commit()
            return True
        except Error as e:
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def complete_hardware_change(req_id, hardware_name, tech_name, admin_id):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            cursor.execute("SELECT hardwareID, quantity FROM hardware WHERE hardwareName = %s LIMIT 1",
                           (hardware_name,))
            row = cursor.fetchone()

            if not row:
                raise Exception(f"Hardware '{hardware_name}' not found.")
            if row[1] <= 0:
                raise Exception(f"Stock Error: {hardware_name} is out of stock.")

            hw_id = row[0]
            cursor.execute("UPDATE hardware SET quantity = quantity - 1 WHERE hardwareID = %s", (hw_id,))

            cursor.execute(
                "INSERT INTO stock_logs (hardwareID, quantityChanged, adminID, reason, dateAdded) VALUES (%s, -1, %s, 'Used for repair', NOW())",
                (hw_id, admin_id))

            query = "UPDATE requests SET status = %s, hardware = %s, validator = %s, dateAction = NOW() WHERE requestID = %s"
            cursor.execute(query, (tech_name, hardware_name, admin_id, req_id))

            conn.commit()
            return True, "Technician sent."

        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()