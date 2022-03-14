import datetime
from enum import IntEnum
import os
import pymssql
import datetime

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from VaccinePatient import *
from COVID19_vaccine import *
from Patient import *
from enums import *
from utils import *

class VaccineReservationScheduler:

    def __init__(self, patientid, vaccine_name):
        self.patientid = patientid
        self.vaccine_name = vaccine_name
        self.slot_status = None
        self.patient = Patient()
        self.vaccine_inventory = Vaccines(self.vaccine_name)
        return

    def PutHoldOnAppointmentSlot(self, cursor, vaccine_status, work_day = None, slot_hour = None, slot_minute = None):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Should return 0 if no slot is available  or -1 if there is a database error'''
        #self.vac_status = 1
        if work_day is None:
            work_day = str(datetime.date.today())
        if slot_hour is None:
            current_time = datetime.datetime.now()
            slot_hour = int(current_time.hour)
        if slot_minute is None:
            current_time = datetime.datetime.now()
            slot_minute = int(current_time.minute)

        appt_query = f"SELECT CaregiverSlotSchedulingId AS apptslotId, CaregiverId AS cgid " \
                             f"FROM CareGiverSchedule WHERE SlotStatus = 0 AND WorkDay = '{work_day}' "\
                             f"AND SlotHour = {slot_hour} AND SlotMinute = {slot_minute}"

        try:
            cursor.execute(appt_query)
            row = cursor.fetchone()
            if row is not None and 'apptslotId' in row and 'cgid' in row:
                slotSchedulingId = row['apptslotId']
                cgid = row['cgid']

                #Update vaccine inventory.
                new_inventory, DosesPerPatient = self.vaccine_inventory.ReserveDoses(1, cursor, VaccineSupplier=None)
                if new_inventory >= DosesPerPatient:
                    #Update Caregiverschedule Table
                    appt_query = f"UPDATE CareGiverSchedule SET SlotStatus = 1 " \
                                     f"WHERE CaregiverSlotSchedulingId = {slotSchedulingId} AND SlotStatus = 0"
                    cursor.execute(appt_query)

                    #Update the patient table.
                    self.patient.updatePatientsTable(self.patientid, vaccine_status, cursor)

                    cursor.connection.commit()
                    return slotSchedulingId, cgid
                else:
                    return 0, 0
            else:
                print("No time slot available.")
                cursor.connection.rollback()
                return 0, 0

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])           
            print("SQL text that resulted in an Error: " + appt_query)
            cursor.connection.rollback()
            return -1, -1

    def ScheduleAppointmentSlot(self, slotid, cursor, vaccine_status):
        '''method that marks a slot on Hold with a definite reservation  
        slotid is the slot that is currently on Hold and whose status will be updated 
        returns the same slotid when the database update succeeds 
        returns 0 if the database update fails
        returns -1 the same slotid when the database command fails
        returns -2 if the slotid parm is invalid '''
        self.slot_status = 2
        if slotid < 1:
            return -2

        #Check if the sloid is in the table. If not, return -2.
        appt_query = f"SELECT * " \
                     f"FROM CareGiverSchedule WHERE SlotStatus = 1 AND CaregiverSlotSchedulingId = {slotid}"
        cursor.execute(appt_query)
        row = cursor.fetchone()
        if row is None:
            return -2

        #Update the Caregiverscheduler Table
        appt_query = f"UPDATE CareGiverSchedule SET SlotStatus = 2 " \
                                 f"WHERE CaregiverSlotSchedulingId = {slotid} AND SlotStatus = 1"
        try:
            cursor.execute(appt_query)

            appt_query = f"SELECT SlotStatus AS status FROM CareGiverSchedule " \
                           f"WHERE CaregiverSlotSchedulingId = {slotid}"

            cursor.execute(appt_query)
            row = cursor.fetchone()
            if row is not None and 'status' in row and row['status'] == 2:
                # Update the patient table.
                self.patient.updatePatientsTable(self.patientid, vaccine_status, cursor)
                cursor.connection.commit()
                return slotid
            else:
                print("Database update failed.")
                cursor.connection.rollback()
                return 0

        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            print("SQL text that resulted in an Error: " + appt_query)
            cursor.connection.rollback()
            return -1

if __name__ == '__main__':
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            clear_tables(sqlClient)
            vrs = VaccineReservationScheduler()

            # get a cursor from the SQL connection
            dbcursor = sqlClient.cursor(as_dict=True)

            # Iniialize the caregivers, patients & vaccine supply
            caregiversList = []
            caregiversList.append(VaccineCaregiver('Carrie Nation', dbcursor))
            caregiversList.append(VaccineCaregiver('Clare Barton', dbcursor))
            caregivers = {}
            for cg in caregiversList:
                cgid = cg.caregiverId
                caregivers[cgid] = cg

            # Add a vaccine and Add doses to inventory of the vaccine
            # Ass patients
            # Schedule the patients
            
            # Test cases done!
            clear_tables(sqlClient)
