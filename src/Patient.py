import pymssql


class Patient:
    def __init__(self):
        self.vaccine_status = None

    def addNewPatient(self, name, bday, address, vaccine_status, cursor):
        try:
            query = f"INSERT INTO Patients OUTPUT INSERTED.PatientID" \
                    f" VALUES ('{name}', '{bday}', '{address}', {vaccine_status})"
            cursor.execute(query)
            row = cursor.fetchone()
            if row is not None and 'PatientID' in row:
                patientid = row['PatientID']
            cursor.connection.commit()
            return patientid

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print(f"Exception code: {db_err.args[0]}")
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            print("SQL text that resulted in an Error: " + query)
            cursor.connection.rollback()
            return db_err



    def updatePatientsTable(self, patientid, vaccine_status, cursor):

        try:
            query = f"UPDATE Patients SET VaccineStatus = {vaccine_status} " \
                    f"WHERE PatientId = {patientid}"
            cursor.execute(query)
            cursor.connection.commit()

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            print("SQL text that resulted in an Error: " + query)
            cursor.connection.rollback()
            return db_err
