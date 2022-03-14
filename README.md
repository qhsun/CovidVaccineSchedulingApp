# CovidVaccineSchedulingApp

This project is to to build a proof-of-concept vaccine scheduling application that can be deployed by medical entities, bringing together care givers, patients and doses of the vaccine in order to administer vaccine doses to those patients to slow the spread of the virus.

This application will support the scheduling of appointments where trained caregivers will administer vaccine doses to patients. The following entity sets associated with vaccine scheduling have been identified:
- Caregivers: these are employees of the health organization administering the vaccines
- Patients: these are customers of the health organization that want to receive the vaccine
- Vaccines: these are vaccine doses in the health organization’s inventory of medical supplies that are on hand and need to be given to the patients.

Associated with each caregiver in the database is a caregiver schedule, where each instance of a potential vaccine administration is maintained as a scheduling slot. To keep things simple in this proof-of-concept application, scheduling slots are defined every fifteen minutes for the duration of a vaccine administration scheduling window, limited to two hours daily initially while vaccine doses are in short supply.

### Methods
- **AddDoses()** which is called to add doses to the vaccine inventory for a particular vaccine
- **ReserveDoses()** which is called to reserve the vaccine doses associated with a specific patient who is being scheduled for vaccine administration.
- **ReserveAppointment (CaregiverSchedulingID, Vaccine, cursor)**, called with the following parameters:    
    a) CaregiverSchedulingID identifying an available time slot in the CaregiverSchedule Table    
    b) an instance of a Vaccine class.  
    c) a cursor object obtained from the pymssql connection.  
    The method would verify that the CaregiverSchedule slot id that is passed as a parameter is currently in the “OnHold” status.
- **ScheduleAppointment()**, which is called to mark the appointments as “Scheduled”, update the Patient’s VaccineStatus field, maintain the Vaccine inventory, update the CaregiverScheduler Table, and any additional tasks required to schedule the appointments for the Caregiver  to administer the vaccine doses to the Patient, ensuring that the database properly reflects the Scheduling Actions.




