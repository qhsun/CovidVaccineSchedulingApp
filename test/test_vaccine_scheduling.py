import unittest
import os
import uuid

import pymssql
from sql_connection_manager import *
from vaccine_reservation_scheduler import  *
from COVID19_vaccine import *
from VaccinePatient import *
from vaccine_caregiver import *
from CovidVaccineScheduler import *
from Patient import *
from enums import *
from utils import *
from datetime import datetime, date, timedelta

class TestVaccines(unittest.TestCase):
    def test_make_vaccine_appt(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                # Create a unique id via uuid to prevent an existing id.
                VaccineName = str(uuid.uuid4())
                caregivername1 = str(uuid.uuid4())
                caregivername2 = str(uuid.uuid4())
                try:
                    # create a new VaccineCaregiver object
                    vaccine = Vaccines(VaccineName)
                    # add 5 doses into the vaccine table
                    new_inventory=5
                    DosesPerPatient = 2
                    DaysBetweenDoses = 21
                    vaccine.AddDoses(new_inventory, cursor, DosesPerPatient, DaysBetweenDoses, VaccineSupplier=None)

                    careGiver1 = VaccineCaregiver(caregivername1, cursor)
                    careGiverId1 = careGiver1.caregiverId
                    schedule = careGiver1.scheduleDates

                    careGiver2 = VaccineCaregiver(caregivername2, cursor)
                    careGiverId2 = careGiver2.caregiverId

                    patientIds = []
                    name = ['a', 'b', 'c', 'd', 'e']
                    bday = ['2020-01-01','2020-01-01','2020-01-01','2020-01-01','2020-01-01']
                    addr = ['addr','addr','addr','addr','addr','addr']
                    prefer_date = schedule
                    prefer_hr = [10, 10, 10, 11, 11]
                    prefer_minute = [0, 15, 30, 45, 0]

                    for i in range(5):
                        scheduler = CovidVaccineScheduler(name[i], bday[i], addr[i], VaccineName, prefer_date[i],
                                                          prefer_hr[i], prefer_minute[i])
                        scheduler.schedule(cursor)
                        patientIds.append(scheduler.patientId)

                    self.successfulVaccineAppointment(patientIds[0], VaccineName, cursor)

                    self.successfulVaccineAppointment(patientIds[1], VaccineName, cursor)

                    self.unsuccessfulVaccineAppointment(patientIds[2], VaccineName, cursor)
                    self.unsuccessfulVaccineAppointment(patientIds[3], VaccineName, cursor)
                    self.unsuccessfulVaccineAppointment(patientIds[4], VaccineName, cursor)
                    # clear the tables after testing, just in-case
                    clear_schedule_tables(sqlClient, VaccineName, careGiverId1, careGiverId2, patientIds)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_schedule_tables(sqlClient, VaccineName, careGiverId1, careGiverId2, patientIds)
                    self.fail(f"{VaccineName} does not exist in database.")
            #cursor.connection.close()

    def successfulVaccineAppointment(self, patientId, vaccineName, cursor):
        query = f"SELECT VaccineStatus FROM Patients WHERE PatientId = {patientId}"
        cursor.execute(query)
        row = cursor.fetchone()
        status = row['VaccineStatus']
        self.assertEqual(status, 5)

        query = f"SELECT * FROM VaccineAppointments WHERE PatientId = {patientId} AND " \
                f"VaccineName = '{vaccineName}'"
        cursor.execute(query)
        row = cursor.fetchall()
        num_row = len(row)
        self.assertEqual(num_row, 2)

        query = f"SELECT VaccineAppointmentId AS apptid FROM VaccineAppointments WHERE PatientId = {patientId}"
        cursor.execute(query)
        rows = cursor.fetchall()
        slot_id1 = rows[0]['apptid']
        slot_id2 = rows[1]['apptid']

        query = f"SELECT SlotStatus FROM CareGiverSchedule WHERE VaccineAppointmentId = {slot_id1}"
        cursor.execute(query)
        row = cursor.fetchone()
        slot_status1 = row['SlotStatus']

        query = f"SELECT SlotStatus FROM CareGiverSchedule WHERE VaccineAppointmentId = {slot_id2}"
        cursor.execute(query)
        row = cursor.fetchone()
        slot_status2 = row['SlotStatus']

        slot_status = [slot_status1, slot_status2]
        self.assertEqual(slot_status, [2,2])

        query = f"SELECT AvailableDoses FROM Vaccines WHERE VaccineName = '{vaccineName}'"
        cursor.execute(query)
        row = cursor.fetchone()
        avail_dose = row['AvailableDoses']
        self.assertEqual(avail_dose, 1)

    def unsuccessfulVaccineAppointment(self, patientId, vaccineName, cursor):
        query = f"SELECT VaccineStatus FROM Patients WHERE PatientId = {patientId}"
        cursor.execute(query)
        row = cursor.fetchone()
        status = row['VaccineStatus']
        self.assertEqual(status, 0)

        query = f"SELECT * FROM VaccineAppointments WHERE PatientId = {patientId} AND " \
                f"VaccineName = '{vaccineName}'"
        cursor.execute(query)
        row = cursor.fetchone()
        self.assertEqual(row, None)

        query = f"SELECT VaccineAppointmentId AS apptid FROM VaccineAppointments WHERE PatientId = {patientId}"
        cursor.execute(query)
        rows = cursor.fetchone()
        self.assertEqual(row, None)

if __name__ == '__main__':
    unittest.main()