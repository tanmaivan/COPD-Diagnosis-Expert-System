import mysql.connector

class ConnectDatabase:
    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 3306
        self._user = "root"
        self._password = "1234"
        self._database = "db_copd"
        self.con = None
        self.cursor = None

    def connect_db(self):
        # Establish a database connection
        self.con = mysql.connector.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password
        )

        # Create a cursor for executing SQL queries
        self.cursor = self.con.cursor(dictionary=True)

    def get_all_info(self):
        self.connect_db()

        sql = "SELECT * FROM tb_patient_info ORDER BY patient_id DESC;"

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            return E
        finally:
            self.con.close()

    def add_info(self, full_name, gender, age, address, phone_number):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for adding information
        sql = """
        INSERT INTO tb_patient_info (full_name, gender, age, address, phone_number) 
        VALUES (%s, %s, %s, %s, %s);
        """

        try:
            # Execute the SQL query for adding information
            self.cursor.execute(sql, (full_name, gender, age, address, phone_number))
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def update_info(self, patient_id, full_name, gender, age, address, phone_number):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for updating information
        sql = f"""
            UPDATE students_info
                SET patient_id='{patient_id}', full_name='{full_name}', gender='{gender}', age='{age}', address='{address}', phone_number='{phone_number}'
                WHERE patient_id={patient_id};
        """

        try:
            # Execute the SQL query for updating information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def delete_info(self, patient_id):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for deleting information
        sql = f"""  
            DELETE FROM tb_patient_info WHERE patient_id={patient_id};
        """

        try:
            # Execute the SQL query for deleting information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()


    
if __name__ == "__main__":
    db = ConnectDatabase()
    try:
        # Test connection
        db.connect_db()
        print("Kết nối thành công!")

        # Test thêm thông tin
        result = db.add_info("Nguyen Van B", "Male", 30, "Hanoi", "0123456789")
        if result is None:
            print("Thêm thông tin thành công!")
        else:
            print("Lỗi:", result)

    except Exception as e:
        print("Lỗi kết nối:", e)
