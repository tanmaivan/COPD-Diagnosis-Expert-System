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

    def get_primary_key(self, table_name):
        self.connect_db()
        sql = f"""
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = '{self._database}' AND TABLE_NAME = '{table_name}' AND COLUMN_KEY = 'PRI';
        """
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result['COLUMN_NAME'] if result else None
        except Exception as E:
            return None
        finally:
            self.con.close()

    def get_all_info(self, table_name):
        self.connect_db()
        
        primary_key = self.get_primary_key(table_name)
        if not primary_key:
            return Exception("Primary key not found for table: " + table_name)

        sql = f"SELECT * FROM `{table_name}` ORDER BY `{primary_key}` DESC;"

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            if err.errno == 2055:
                self.connect_db()
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                return result
            else:
                return err
        except Exception as E:
            return E
        finally:
            self.con.close()

    def add_info(self, table_name, data):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for adding information
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.con.commit()

        except Exception as E:
            self.con.rollback()
            return E

        finally:
            self.con.close()

    def delete_info(self, table_name, primary_key_column, id):
        self.connect_db()
        sql = f"DELETE FROM `{table_name}` WHERE `{primary_key_column}` = %s;"
        try:
            self.cursor.execute(sql, (id,))
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

