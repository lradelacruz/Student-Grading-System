import connect_db

print(connect_db.myConnection)


class CRUD:
    def __init__(self, table):
        self.cursorObject = connect_db.myConnection.cursor()
        self.table = table

    def createRows(self, data):
        self.recon()
        try:
            with self.cursorObject as cur:
                # data format : (ID,Name,Course,Year,Prelim,Midterm,Finals,Remarks)
                cur.executemany('INSERT INTO ' + self.table + ' VALUES(%s, %s, %s, %s, %s, %s, %s,%s)', data)
                cur.close()
                for data in data:
                    print('new student inserted : {}'.format(data[0]))
        except Exception as e:
            print("Exception occurred:{}".format(e))

    def createRow(self, data):
        self.recon()
        try:
            with self.cursorObject as cur:
                # data format : (Name,Course,Year,Prelim,Midterm,Finals,Remarks)
                cur.execute('INSERT INTO ' + self.table + ' VALUES(0, %s, %s, %s, %s, %s, %s, %s)',
                            (data[0], data[1], int(data[2]), int(data[3]), int(data[4]), int(data[5]), data[6]))
                cur.close()
                print('new student data inserted : {}'.format(data[1]))
        except Exception as e:
            print("Exception occurred:{}".format(e))

    def readData(self):
        self.recon()
        try:
            with self.cursorObject as cur:
                cur.execute('SELECT * FROM ' + self.table)  # DB query
                rows = cur.fetchall()  # get all data
                for row in rows:
                    print(
                        f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]} {row[7]}')
        except Exception as e:
            print("Exception occurred:{}".format(e))

    def readSingleData(self, clause):
        self.recon()
        try:
            with self.cursorObject as cur:
                cur.execute('SELECT * FROM ' + self.table + ' ' + clause)  # DB query
                rows = cur.fetchall()  # get all data
                for row in rows:
                    print(
                        f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]} {row[7]}')
        except Exception as e:
            print("Exception occurred:{}".format(e))

    def updateData(self, data):
        self.recon()
        try:
            if data[0] == "ID":  # because ID is INT Data
                updatequery = "update " + self.table + " set " + data[0] + " = " + data[1] + " where ID = '" + data[
                    2] + "'"
                self.cursorObject.execute(updatequery)
            else:  # for STRING Data
                updatequery = "update " + self.table + " set " + data[0] + " = '" + data[1] + "' where ID = '" + data[
                    2] + "'"
                self.cursorObject.execute(updatequery)
        except Exception as e:
            print("Exception occurred:{}".format(e))

    def deleteData(self, data):
        self.recon()
        try:
            deletequery = "delete from " + self.table + " where Name = '" + data + "'"
            self.cursorObject.execute(deletequery)
            print("Deleted!")
        except Exception as e:
            print("Exception occurred:{}".format(e))

    def getRows(self):
        self.cursorObject.execute(f"Select * FROM {self.table}")
        rows = self.cursorObject.fetchall()
        return rows

    # utility functions
    def set_Table(self, table):
        self.table = table

    def recon(self):
        self.cursorObject = connect_db.myConnection.cursor()

    def closeConn(self):
        self.cursorObject.close()
