import sqlite3
from sqlite3 import Error
import xlrd
import time
from time import strftime
import os
from datetime import datetime

tm = time.localtime()
tmStmp = "{}{}{}".format(tm.tm_mday, tm.tm_mon, tm.tm_year)


class Database():
    def __init__(self):
        if not os.path.exists("database/"):
            os.makedirs("database/")

        # .db file
        self.db = ""

    # Insert into database
    def insert_into_database(self, tableName, conn, data):

        if conn is not None:
            try:
                c = conn.execute("select * from {}".format(tableName))
                fields = tuple([des[0] for des in c.description][:])

                if "id" in fields:
                    fields = tuple(list(fields)[1:])
                cur = conn.cursor()
                cur.execute(
                    """
					INSERT INTO {}
					{} VALUES {}
					""".format(
                        tableName, fields, data
                    )
                )
                conn.commit()
                return True
            except Error as e:
                print("Error in data insertion: {}".format(e))
        return None

    # Update Database
    def update_database(self, tableName, conn, fields, field_vals, ref, index):
        if conn is not None:
            try:
                cur = conn.cursor()
                if not isinstance(fields, tuple) and not isinstance(fields, list):
                    fields = list([fields])
                    field_vals = list([field_vals])

                for field, field_val in zip(fields, field_vals):

                    cur.execute(
                        """
							UPDATE {}
							SET {}= ? WHERE {}= ?
							""".format(
                            tableName, field, ref
                        ),
                        (field_val, index),
                    )
                    conn.commit()
                return True
            except Exception as e:
                print("Error in updating data: {}".format(e))
        return None

    # Delete from Database
    def delete_from_database(self, tableName, conn, condition):
        if conn is not None:
            try:
                cur = conn.cursor()
                # just to track if deletion was successful
                count= len(cur.execute("""
						SELECT * FROM {} WHERE {}
						""".format(
                        tableName, condition)
                ).fetchall())
                if not count:
                    return False
                cur.execute(
                    """
						DELETE FROM {} WHERE {}
						""".format(
                        tableName, condition
                    )
                )
                conn.commit()
                return True
            except Error as e:
                print("Error in deleting data: {}".format(e))
        return False

    # Search in the database
    def search_from_database(self, tableName, conn, prop, value, order_by="reg"):
        if conn is not None:
            try:
                cur = conn.cursor()
                #print("cur: {}".format(cur))
                filtered_list = cur.execute(
                    """
							SELECT * FROM {} WHERE {} LIKE ? ORDER BY {};
						""".format(
                        tableName, prop, order_by
                    ),
                    (str(value) + "%",),
                ).fetchall()
                return filtered_list
            except Error as e:
                print("Error in searching: {}".format(e))

            return None

    # connect database
    def connect_database(self, db_file):
        try:
            conn = sqlite3.connect("database/" + db_file)
            return conn

        except Error as e:
            print("Error in database: {}".format(e))

        return None

    # create table
    def create_table(self, table, conn):

        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(table)
                conn.commit()

            except Error as e:
                print("Error in creating table: {}".format(e))

        else:
            print("conn is none")

    def findTables(self, db_file):
        conn = self.connect_database(db_file)
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [each[0] for each in cur.fetchall()]
        # conn.close()

    def readFile(self, db_file, table, tableName, file_name, **kwargs):

        table = table.format(tableName)
        try:
            wb = xlrd.open_workbook(file_name)
            sheet = wb.sheet_by_index(0)
            rows = sheet.nrows

            conn = self.connect_database(db_file)

            if conn is not None:
                self.create_table(table, conn)

                for i in range(1, rows):
                    data = (
                        sheet.cell_value(i, 1),
                        sheet.cell_value(i, 2),
                        kwargs["course"],
                        kwargs["stream"],
                        kwargs["fromYear"] + "-" + kwargs["toYear"],
                        kwargs["fee"],
                    )

                    self.insert_into_database(tableName, conn, data)
                return True
        
            return False
        except: return False

    def addData(self, db_file, table, tableName, data):

        table = table.format(tableName)
        conn = self.connect_database(db_file)

        if conn is not None:
            self.create_table(table, conn)
            return self.insert_into_database(tableName, conn, data)
        return None

    def extractAllData(self, db_file, tableName, order_by="reg"):
        conn = self.connect_database(db_file)

        if conn is not None:
            cur = conn.execute(
                "SELECT * FROM {} ORDER BY {}".format(tableName, order_by)
            )
            return cur.fetchall()
        return None


if __name__ == "__main__":

    db = Database()
    # db.readFile("C:\\Users\\Anand Kumar\\Desktop\\project\\student.xlsx", "year_2017_2021")
    conn = db.connect_database()
    # db.delete_from_database("2017_2021",conn, 24)
    print(db.search_from_database("year_2022_2019", conn, "name", "ajit"))
