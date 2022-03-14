import pymssql
from sql_connection_manager import *
import traceback

class UpdatingVaccineError(Exception):
    pass

class ReserveVaccineError(Exception):
    pass


class Vaccines:

    def __init__(self, VaccineName):
        self.VaccineName = VaccineName

    def AddDoses(self, new_inventory, cursor, DosesPerPatient, DaysBetweenDoses, VaccineSupplier=None):
        if VaccineSupplier == None:
            VaccineSupplier = self.VaccineName
        select_query = f"SELECT AvailableDoses AS inventory, TotalDoses AS total" \
                       f" FROM Vaccines WHERE VaccineName = '{self.VaccineName}'"
        try:
            cursor.execute(select_query)
            row = cursor.fetchone()

            if row is not None and 'inventory' in row:
                old_inventory = int(row['inventory'])
                old_total = row['total']
                new_inventory = old_inventory + new_inventory
                new_total = old_total + new_inventory
                update_query = f"UPDATE Vaccines SET AvailableDoses = {new_inventory}, TotalDoses = {new_total}" \
                               f"FROM Vaccines WHERE VaccineName = '{self.VaccineName}'"
                cursor.execute(update_query)
            else:
                print()
                insert_query = f"INSERT INTO Vaccines VALUES ('{self.VaccineName}', '{VaccineSupplier}', " \
                               f"{new_inventory}, 0, {new_inventory}, {DosesPerPatient}, {DaysBetweenDoses})"
                cursor.execute(insert_query)

            cursor.connection.commit()

        except UpdatingVaccineError as updateexp:
            print("Database Programming Error in SQL Query processing for updating vaccine inventory! ")
            print("Exception code: " + str(updateexp.args[0]))
            print(updateexp.args)
            print("SQL query that resulted in an Error: " + select_query)
            cursor.connection.rollback()
            raise updateexp

        return

    def ReserveDoses(self, DosesPerPatient, cursor, VaccineSupplier=None):
        if VaccineSupplier == None:
            VaccineSupplier = self.VaccineName

        reserve_query = f"SELECT AvailableDoses AS inventory, TotalDoses AS total, DosesPerPatient" \
                       f" FROM Vaccines WHERE VaccineName = '{self.VaccineName}'"
        try:
            cursor.execute(reserve_query)
            row = cursor.fetchone()
            if row is not None and 'inventory' in row:
                old_inventory = row['inventory']
                old_total = row['total']
                doses_needed = row['DosesPerPatient']
                if old_inventory < doses_needed:
                    print("No vaccine available!")
                    return 0, 1
                else:
                    new_inventory = old_inventory - DosesPerPatient
                    new_total = old_total - DosesPerPatient
                    update_query = f"UPDATE Vaccines SET AvailableDoses = {new_inventory}, TotalDoses = {new_total} " \
                                   f"FROM Vaccines WHERE VaccineName = '{self.VaccineName}'"
                    cursor.execute(update_query)
                    cursor.connection.commit()
                    return new_inventory, DosesPerPatient
            else:
                cursor.connection.rollback()
                return 0, 1
                # raise ReserveVaccineError("No vaccine available!")
        except ReserveVaccineError as reserveexp:
            print("Database Programming Error in SQL Query processing for reserving vaccine!")
            print("Exception code: " + str(reserveexp.args[0]))
            print(reserveexp.args)
            print("SQL query that resulted in an Error: " + reserve_query)
            cursor.connection.rollback()
            return 0, 1
        return

if __name__ == '__main__':
    with SqlConnectionManager(Server=os.getenv("Server"),
                              DBname=os.getenv("DBName"),
                              UserId=os.getenv("UserID"),
                              Password=os.getenv("Password")) as sqlClient:
        with sqlClient.cursor(as_dict=True) as cursor:
            vacc = Vaccines("Pfizer")
            vacc.AddDoses(150, cursor, 2, 21, VaccineSupplier=None)
            vacc.ReserveDoses(2, cursor, VaccineSupplier = None)
            cursor.connection.close()