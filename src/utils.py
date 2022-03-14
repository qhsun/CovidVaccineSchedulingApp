def clear_tables(client):
    sqlQuery = '''
               Truncate Table CareGiverSchedule
               DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 0)
               Delete From Caregivers
               DBCC CHECKIDENT ('Caregivers', RESEED, 0)
               '''
    client.cursor().execute(sqlQuery)
    client.commit()


def clear_schedule_tables(client, VaccineName, careGiverId1, careGiverId2, patientIds):
    sqlQuery = f"Delete From Vaccines WHERE VaccineName = '{VaccineName}'"
    client.cursor().execute(sqlQuery)
    client.commit()

    sqlQuery = f"Delete From VaccineAppointments WHERE VaccineName = '{VaccineName}'"
    client.cursor().execute(sqlQuery)
    client.commit()

    sqlQuery = f"Delete From CareGiverSchedule WHERE CareGiverId = {careGiverId1}"
    client.cursor().execute(sqlQuery)
    client.commit()

    sqlQuery = f"Delete From Caregivers WHERE CaregiverId = {careGiverId1}"
    client.cursor().execute(sqlQuery)
    client.commit()

    sqlQuery = f"Delete From CareGiverSchedule WHERE CareGiverId = {careGiverId2}"
    client.cursor().execute(sqlQuery)
    client.commit()

    sqlQuery = f"Delete From Caregivers WHERE CaregiverId = {careGiverId2}"
    client.cursor().execute(sqlQuery)
    client.commit()

    for patientId in patientIds:
        sqlQuery = f"Delete From Patients WHERE PatientId = {patientId}"
        client.cursor().execute(sqlQuery)
        client.commit()
