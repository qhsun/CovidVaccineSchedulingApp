import unittest
import os
import uuid

from sql_connection_manager import SqlConnectionManager
from utils import *
from COVID19_vaccine import *

class TestVaccines(unittest.TestCase):
    def test_insert_vaccines(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                # Create a unique id via uuid to prevent an existing id.
                VaccineName = str(uuid.uuid4())
                try:
                    # create a new VaccineCaregiver object
                    vaccine = Vaccines(VaccineName)
                    # check if the patient is correctly inserted into the database
                    new_inventory=100
                    DosesPerPatient = 2
                    DaysBetweenDoses = 21
                    vaccine.AddDoses(new_inventory, cursor, DosesPerPatient, DaysBetweenDoses, VaccineSupplier=None)
                    select_query = f"SELECT AvailableDoses AS inventory FROM Vaccines WHERE VaccineName = '{VaccineName}'"
                    cursor.execute(select_query)
                    row = cursor.fetchone()
                    if row is not None and 'inventory' in row:
                        inventory = row['inventory']
                        self.assertEqual(inventory, 100)
                    else:
                        self.fail(f"{VaccineName} does not exist in database.")
                    # clear the tables after testing, just in-case
                    clear_vaccines_tables(sqlClient, VaccineName)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_vaccines_tables(sqlClient, VaccineName)
                    self.fail(f"{VaccineName} does not exist in database.")
            #cursor.connection.close()

    def test_update_vaccines(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                # Create a unique id via uuid to prevent an existing id.
                VaccineName = str(uuid.uuid4())
                try:
                    # create a new VaccineCaregiver object
                    vaccine = Vaccines(VaccineName)
                    # check if the patient is correctly inserted into the database
                    new_inventory1 = 150
                    DosesPerPatient = 2
                    DaysBetweenDoses = 21
                    AvailableDoses = new_inventory1
                    TotalDoses = new_inventory1
                    insert_query = f"INSERT INTO Vaccines Values ('{VaccineName}', '{VaccineName}', " \
                                   f"{AvailableDoses}, 0, {TotalDoses}, {DosesPerPatient}, {DaysBetweenDoses})"
                    cursor.execute(insert_query)
                    new_inventory2 = 100
                    vaccine.AddDoses(new_inventory2, cursor, DosesPerPatient, DaysBetweenDoses, VaccineSupplier=None)
                    select_query = f"SELECT AvailableDoses AS inventory FROM Vaccines WHERE VaccineName = '{VaccineName}'"
                    cursor.execute(select_query)
                    row = cursor.fetchone()
                    if row is not None and 'inventory' in row:
                        inventory = row['inventory']
                        self.assertEqual(inventory, new_inventory1 + new_inventory2)
                    else:
                        self.fail(f"Could not update {VaccineName} inventory in database.")
                    # clear the tables after testing, just in-case
                    clear_vaccines_tables(sqlClient, VaccineName)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_vaccines_tables(sqlClient, VaccineName)
                    self.fail(f"Could not update {VaccineName} inventory in database.")
            #cursor.connection.close()

    def test_reserve_nonexist_vaccines(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                # Create a unique id via uuid to prevent an existing id.
                VaccineName = str(uuid.uuid4())
                # create a new VaccineCaregiver object
                vaccine = Vaccines(VaccineName)
                # check if the patient is correctly inserted into the database
                DosesPerPatient = 2
                with self.assertRaises(ReserveVaccineError):
                    vaccine.ReserveDoses(DosesPerPatient, cursor, VaccineSupplier=None)
            #cursor.connection.close()

    def test_reserve_exist_vaccines(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                # Create a unique id via uuid to prevent an existing id.
                VaccineName = str(uuid.uuid4())
                try:
                    # create a new VaccineCaregiver object
                    vaccine = Vaccines(VaccineName)
                    # check if the patient is correctly inserted into the database
                    new_inventory = 120
                    DosesPerPatient = 2
                    DaysBetweenDoses = 28
                    AvailableDoses = new_inventory
                    TotalDoses = new_inventory
                    insert_query = f"INSERT INTO Vaccines Values ('{VaccineName}', '{VaccineName}', " \
                                   f"{AvailableDoses}, 0, {TotalDoses}, {DosesPerPatient}, {DaysBetweenDoses})"
                    cursor.execute(insert_query)
                    vaccine.ReserveDoses(DosesPerPatient, cursor, VaccineSupplier=None)
                    select_query = f"SELECT AvailableDoses AS inventory FROM Vaccines WHERE VaccineName = '{VaccineName}'"
                    cursor.execute(select_query)
                    row = cursor.fetchone()
                    if row is not None and 'inventory' in row:
                        inventory = row['inventory']
                        self.assertEqual(inventory, new_inventory-DosesPerPatient)
                    else:
                        self.fail(f"Could not reserve {VaccineName}.")
                    # clear the tables after testing, just in-case
                    clear_vaccines_tables(sqlClient, VaccineName)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_vaccines_tables(sqlClient, VaccineName)
                    self.fail(f"Could not reserve {VaccineName}.")
            #cursor.connection.close()
            
if __name__ == '__main__':
    unittest.main()