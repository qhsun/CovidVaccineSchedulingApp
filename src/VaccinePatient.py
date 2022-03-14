import pymssql
from sql_connection_manager import *
from COVID19_vaccine import *

class SlotNotOnHoldError(Exception):
    pass

class ApptReservationNotAllowedError(Exception):
    pass

class VaccinePatient:

    def __init__(self, PatientId, VaccineName):
        self.PatientId = PatientId
        self.Vaccine = Vaccines(VaccineName)
        self.apptduration = None

    #Return DaysBetweenDoses, DosesPerPatient
    def ReserveAppointment(self, CaregiverSchedulingId, Vaccine, cursor):
        query = f"SELECT SlotStatus AS status FROM CareGiverSchedule " \
                     f"WHERE CaregiverSlotSchedulingId = {CaregiverSchedulingId}"
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            slotstatus = -1
            if row is not None and 'status' in row and row['status'] == 1:
                slotstatus = 2
            else:
                print("The slot status is not on hold.")
                # raise SlotNotOnHoldError

            query = f"SELECT AvailableDoses AS avail_doses, DosesPerPatient, DaysBetweenDoses FROM Vaccines " \
                            f"WHERE VaccineName = '{self.Vaccine.VaccineName}'"
            cursor.execute(query)
            vacc_row = cursor.fetchone()
            ReservationDate = None
            allowedNumberOfDoses = 0
            DaysBetweenDoses = 0

            if vacc_row is not None and 'avail_doses' in vacc_row and 'DaysBetweenDoses' in vacc_row and 'DosesPerPatient' in vacc_row:
                allowedNumberOfDoses = vacc_row['DosesPerPatient']
                DaysBetweenDoses = vacc_row['DaysBetweenDoses']
                query = f"SELECT CaregiverId, WorkDay, SlotHour, SlotMinute FROM CareGiverSchedule " \
                        f"WHERE CaregiverSlotSchedulingId = {CaregiverSchedulingId}"
                cursor.execute(query)
                row = cursor.fetchone()

                if row is not None and 'CaregiverId' in row and 'WorkDay' in row and 'SlotHour' in row and 'SlotMinute' in row:
                    CaregiverId = row['CaregiverId']
                    ReservationDate = row['WorkDay']
                    ReservationStartHour = row['SlotHour']
                    ReservationStartMinute = row['SlotMinute']
                    if vacc_row['avail_doses'] >= 100:
                        self.apptduration = 15
                    else:
                        self.apptduration = 120

                    query = f"SELECT COUNT(*) AS cnt FROM VaccineAppointments WHERE PatientId = {self.PatientId} AND " \
                            f"VaccineName = '{self.Vaccine.VaccineName}' AND SlotStatus <> 4"
                    cursor.execute(query)
                    row = cursor.fetchone()
                    if row is None or row['cnt'] == 0:
                        DoseNumber = 1
                        query = f"INSERT INTO VaccineAppointments VALUES ('{self.Vaccine.VaccineName}', {self.PatientId}, {CaregiverId}, " \
                                f"'{ReservationDate}', {ReservationStartHour}, {ReservationStartMinute}, {self.apptduration}, " \
                                f" {slotstatus}, Null, {DoseNumber})"
                        cursor.execute(query)

                        query = f"SELECT VaccineAppointmentId AS vac_appt_id, CaregiverId, ReservationDate, ReservationStartHour, ReservationStartMinute " \
                                f"FROM VaccineAppointments " \
                                f"WHERE PatientId = {self.PatientId} AND DoseNumber = {DoseNumber}"
                        cursor.execute(query)
                        row = cursor.fetchone()
                        if row is not None:
                            caregiver = row['CaregiverId']
                            vac_appt_id = row['vac_appt_id']
                            workday = row['ReservationDate']
                            slothr = row['ReservationStartHour']
                            slotminute = row['ReservationStartMinute']
                        query = f"UPDATE CareGiverSchedule SET VaccineAppointmentId = {vac_appt_id} " \
                                f"WHERE CaregiverId = {caregiver} AND WorkDay = '{workday}' AND SlotHour = {slothr} AND SlotMinute = {slotminute}"
                        cursor.execute(query)
                    else:
                        count = row['cnt']
                        if count < allowedNumberOfDoses:
                            DoseNumber = count + 1
                            query = f"INSERT INTO VaccineAppointments VALUES ('{self.Vaccine.VaccineName}', {self.PatientId}, {CaregiverId}, " \
                                    f"'{ReservationDate}', {ReservationStartHour}, {ReservationStartMinute}, {self.apptduration}, " \
                                    f" {slotstatus}, Null, {DoseNumber})"
                            cursor.execute(query)

                            query = f"SELECT VaccineAppointmentId AS vac_appt_id, CaregiverId, ReservationDate, ReservationStartHour, ReservationStartMinute " \
                                    f"FROM VaccineAppointments " \
                                    f"WHERE PatientId = {self.PatientId} AND DoseNumber = {DoseNumber}"
                            cursor.execute(query)
                            row = cursor.fetchone()
                            if row is not None:
                                caregiver = row['CaregiverId']
                                vac_appt_id = row['vac_appt_id']
                                workday = row['ReservationDate']
                                slothr = row['ReservationStartHour']
                                slotminute = row['ReservationStartMinute']
                            query = f"UPDATE CareGiverSchedule SET VaccineAppointmentId = {vac_appt_id} " \
                                    f"WHERE CaregiverId = {caregiver} AND WorkDay = '{workday}' AND SlotHour = {slothr} AND SlotMinute = {slotminute}"
                            cursor.execute(query)

                        else:
                            print("Patient is either fully vaccinated or successfully scheduled.")
                            cursor.connection.rollback()
                            raise ApptReservationNotAllowedError
            cursor.connection.commit()
            return ReservationDate, allowedNumberOfDoses, DaysBetweenDoses

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            print("SQL text that resulted in an Error: " + query)
            cursor.connection.rollback()
            raise db_err

