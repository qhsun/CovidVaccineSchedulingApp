import pymssql
from sql_connection_manager import *
from vaccine_reservation_scheduler import  *
from COVID19_vaccine import *
from VaccinePatient import *
from vaccine_caregiver import *
from Patient import *
from enums import *
from utils import *
from datetime import datetime, date, timedelta

class VaccineNotExistError(Exception):
    pass

class InvalidPreferrenceError(Exception):
    pass


class CovidVaccineScheduler:

    def __init__(self, name, bday, address, prefer_vaccinename, prefer_date, prefer_hr, prefer_minute):
        self.name = name
        self.bday = bday
        self.address = address
        self.prefer_vaccinename = prefer_vaccinename
        self.prefer_date = prefer_date
        self.prefer_hr = prefer_hr
        self.prefer_minute = prefer_minute
        self.patient = Patient()
        self.patientId = None
        return

    # pass user input as parameters
    def gettwoslots(self, cursor, vaccine_reservation_scheduler):
        #Put the prefered date on hold
        period = None
        self.prefer_date = datetime.strptime(self.prefer_date,"%Y-%m-%d").date() #Convert str to datetime
        try:
            query = f"SELECT DaysBetweenDoses AS period, DosesPerPatient AS dose_needed" \
                    f" FROM Vaccines WHERE VaccineName = '{self.prefer_vaccinename}'"
            cursor.execute(query)
            row = cursor.fetchone()
            if row is not None and 'period' in row and 'dose_needed' in row:
                period = row['period']
                dose_needed = row['dose_needed']
            else:
                print('Prefered Vaccine not exists.')
                cursor.connection.rollback()
                raise VaccineNotExistError

            slot_id1, cgid1 = vaccine_reservation_scheduler.PutHoldOnAppointmentSlot(cursor,vaccine_status = 1,
                                                                              work_day=self.prefer_date,
                                                                              slot_hour=self.prefer_hr,
                                                                              slot_minute=self.prefer_minute)
            slot_id2, cgid2 = None, None
            if dose_needed == 2:
                addDays = timedelta(days=period)
                second_date = self.prefer_date + addDays
                # Do we need to get prefer_hr and prefer_minute again?
                slot_id2, cgid2 = vaccine_reservation_scheduler.PutHoldOnAppointmentSlot(cursor, vaccine_status = 4,
                                                                                work_day=second_date,
                                                                                slot_hour=self.prefer_hr,
                                                                                slot_minute=self.prefer_minute)
            if slot_id1 not in [0, -1] and slot_id2 not in [0, -1]:
                print("Proceed to make the reservation for both doses.")
                return slot_id1, cgid1, slot_id2, cgid2
            else:
                print('No time available on prefered date and time. Please try another date/time.')
                cursor.connection.rollback()
                return -1, -1, -1, -1
                #raise InvalidPreferrenceError

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            #print("SQL text that resulted in an Error: " + query)
            cursor.connection.rollback()
            return db_err

    def schedule(self, cursor):
        self.patientId = self.patient.addNewPatient(self.name, self.bday, self.address, 0, cursor)
        vaccine_reservation_scheduler = VaccineReservationScheduler(self.patientId, self.prefer_vaccinename)
        # Get two available time slots, put them on hold, update patient table and vaccine inventory.
        slot_id1, cgid1, slot_id2, cgid2 = self.gettwoslots(cursor, vaccine_reservation_scheduler)
        Vaccine = Vaccines(self.prefer_vaccinename)
        vaccine_patient_appt_table = VaccinePatient(self.patientId, self.prefer_vaccinename)
        # Put the reservation on the appointment table.
        ReservationDate1, allowedNumberOfDoses1, DaysBetweenDoses1 = \
            vaccine_patient_appt_table.ReserveAppointment(slot_id1, Vaccine, cursor)

        # Schedule the vaccine reservation for the two time slots.
        vaccine_reservation = VaccineReservationScheduler(self.patientId, self.prefer_vaccinename)
        scheduled_slot_id1 = vaccine_reservation.ScheduleAppointmentSlot(slot_id1, cursor, vaccine_status=2)

        # Put the reservation on the appointment table.
        # ReservationDate1, allowedNumberOfDoses1, DaysBetweenDoses1 = \
        #     vaccine_patient_appt_table.ReserveAppointment(slot_id1, Vaccine, cursor)

        if slot_id2 is not None and cgid2 is not None:
            ReservationDate2, allowedNumberOfDoses2, DaysBetweenDoses2 = \
                vaccine_patient_appt_table.ReserveAppointment(slot_id2, Vaccine, cursor)
            scheduled_slot_id2 = vaccine_reservation.ScheduleAppointmentSlot(slot_id2, cursor, vaccine_status=5)
            # ReservationDate2, allowedNumberOfDoses2, DaysBetweenDoses2 = \
            #     vaccine_patient_appt_table.ReserveAppointment(slot_id2, Vaccine, cursor)

if __name__ == '__main__':
    with SqlConnectionManager(Server=os.getenv("Server"),
                              DBname=os.getenv("DBName"),
                              UserId=os.getenv("UserID"),
                              Password=os.getenv("Password")) as sqlClient:
        with sqlClient.cursor(as_dict=True) as cursor:
            name = 'x'
            bday = '1988-05-01'
            address = 'add'
            prefer_vaccinename = 'Pfizer'
            prefer_date = '2021-05-02'
            prefer_hr = 9
            prefer_minute = 0
            CovidVaccineScheduler(name, bday, address, prefer_vaccinename, prefer_date, prefer_hr, prefer_minute).schedule(cursor)



