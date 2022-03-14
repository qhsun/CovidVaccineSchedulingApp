from enum import IntEnum


class AppointmentStatus (IntEnum):
    OPEN = 0
    ONHOLD = 1
    SCHEDULED = 2
    COMPLETED = 3
    MISSED = 4

class PatientAppointmentStatus(IntEnum):
    NEW = 0
    QUEUEDFORFIRSTDOSE = 1
    FIRSTDOSESCHEDULED = 2
    FIRSTDOSEADMINISTRED = 3
    QUEUEDFORSECONDDOSE = 4
    SECONDDOSESCHEDULED = 5
    SECONDDOSEADMINISTERED = 6
    VACCINATIONCOMPLETE = 7