from models.database import get_connection
from mysql.connector import Error


class AdminModel:
    @staticmethod
    def login(admin_id, password):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Note: Your schema uses adminID and password
            query = "SELECT adminID, Fn FROM admin WHERE adminID = %s AND password = %s"
            cursor.execute(query, (admin_id, password))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Login Error: {e}")
            return None

    @staticmethod
    def get_all_computers():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                    SELECT 
                        c.pcNo, 
                        IFNULL(CONCAT_WS(' ', e.Fn, e.Mn, e.Ln), 'Unassigned') AS AssignedTo, 
                        c.status 
                    FROM computer c
                    LEFT JOIN employee e ON c.assignedEmp = e.employeeID
                """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            raise e


    @staticmethod
    def get_hardware_inventory():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT brand, quantity FROM hardware ORDER BY hardwareID ASC"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            raise e

    @staticmethod
    def create_new_computer(admin_id):
        conn = get_connection()
        cursor = conn.cursor()

        required_hardware = ["Monitor", "Keyboard & Mouse", "GPU", "Motherboard", "RAM"]

        try:
            conn.start_transaction()

            for part in required_hardware:
                cursor.execute("SELECT quantity, hardwareID FROM hardware WHERE hardwareName = %s LIMIT 1", (part,))
                row = cursor.fetchone()

                if not row:
                    raise Exception(f"Configuration Error: hardwareName '{part}' not found in DB.")

                if row[0] <= 0:
                    raise Exception(f"Build Failed: {part} is currently out of stock.")

            for part in required_hardware:
                cursor.execute("SELECT hardwareID FROM hardware WHERE hardwareName = %s", (part,))
                hw_id = cursor.fetchone()[0]

                cursor.execute("UPDATE hardware SET quantity = quantity - 1 WHERE hardwareID = %s", (hw_id,))

                cursor.execute(
                    "INSERT INTO stock_logs (hardwareID, quantityChanged, adminID, dateAdded) VALUES (%s, -1, %s, NOW())",
                    (hw_id, admin_id)
                )

            cursor.execute("INSERT INTO computer (status, dateAssigned) VALUES ('Available', NULL)")

            conn.commit()
            return True, "Successfully created a new computer! Inventory updated."

        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_hardware_stock(hardware_name, amount, admin_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT hardwareID FROM hardware WHERE hardwareName = %s LIMIT 1", (hardware_name,))
            row = cursor.fetchone()

            if row:
                hw_id = row[0]
                cursor.execute("UPDATE hardware SET quantity = quantity + %s WHERE hardwareID = %s", (amount, hw_id))
                cursor.execute(
                    "INSERT INTO stock_logs (hardwareID, quantityChanged, adminID, dateAdded) VALUES (%s, %s, %s, NOW())",
                    (hw_id, amount, admin_id))
                conn.commit()
            else:
                print(f"ERROR: Hardware '{hardware_name}' not found.")

            cursor.close()
            conn.close()
        except Error as e:
            raise e

    @staticmethod
    def get_stock_logs():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT 
                    CONCAT(h.hardwareName, ' - ', h.brand), 
                    sl.quantityChanged, 
                    CONCAT(a.Fn, ' ', a.Ln), 
                    DATE_FORMAT(sl.dateAdded, '%Y-%m-%d %H:%i:%s')
                FROM stock_logs sl
                JOIN hardware h ON sl.hardwareID = h.hardwareID
                JOIN admin a ON sl.adminID = a.adminID
                ORDER BY sl.dateAdded DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            raise e

    @staticmethod
    def get_dashboard_kpis():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            stats = {}

            cursor.execute("SELECT COUNT(*) FROM computer WHERE assignedEmp IS NOT NULL")
            res = cursor.fetchone()
            stats['active_setups'] = res[0] if res else 0

            cursor.execute("SELECT IFNULL(SUM(quantity), 0) FROM hardware")
            res = cursor.fetchone()
            stats['total_items'] = res[0] if res else 0

            cursor.execute("SELECT COUNT(*) FROM computer WHERE assignedEmp IS NULL")
            res = cursor.fetchone()
            stats['available_pcs'] = res[0] if res else 0

            cursor.close()
            conn.close()
            return stats
        except Exception as e:
            print(f"KPI Error: {e}")
            return {'active_setups': 0, 'total_items': 0, 'available_pcs': 0}

    @staticmethod
    def get_graph_data():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT CONCAT(hardwareName, ' - ', brand), quantity FROM hardware"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            return []

    @staticmethod
    def get_all_requests():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                    SELECT r.pcNo, e.employeeID, CONCAT(e.Fn, ' ', e.Ln), r.hardware, r.reason, r.requestID 
                    FROM requests r
                    JOIN employee e ON r.employeeID = e.employeeID
                    WHERE r.status = 'Pending'
                """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            raise e

    @staticmethod
    def update_request_status(request_id, status, admin_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE requests SET status = %s, validator = %s WHERE requestID = %s"
            cursor.execute(query, (status, admin_id, request_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            raise e

    @staticmethod
    def get_request_history():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                    SELECT 
                        r.pcNo, 
                        r.employeeID, 
                        CONCAT(e.Fn, ' ', e.Ln) AS EmployeeName, 
                        r.hardware, 
                        r.status, 
                        r.dateAction, 
                        IFNULL(CONCAT(a.Fn, ' ', a.Ln), r.validator) AS ValidatorName
                    FROM requests r
                    JOIN employee e ON r.employeeID = e.employeeID
                    LEFT JOIN admin a ON r.validator = a.adminID
                    WHERE r.status != 'Pending'
                    ORDER BY r.dateAction DESC
                """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            raise e

    @staticmethod
    def get_all_setups():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT 
                    e.employeeID, 
                    CONCAT(e.Fn, ' ', e.Mn, ' ', e.Ln) AS Fullname, 
                    c.pcNo, 
                    c.dateAssigned 
                FROM computer c
                INNER JOIN employee e ON c.assignedEmp = e.employeeID
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            raise e