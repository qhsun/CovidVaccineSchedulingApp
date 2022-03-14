DROP PROCEDURE InitDataModel;

CREATE PROCEDURE InitDataModel
AS
CREATE TABLE Caregivers(
    cgid INT NOT NULL IDENTITY PRIMARY KEY,
    cgname VARCHAR(30) NOT NULL
);

CREATE TABLE Patients(
    pid INT NOT NULL IDENTITY PRIMARY KEY,
    pname VARCHAR(30) NOT NULL,
    pbday DATE,
    occupation VARCHAR(30)
);

CREATE TABLE Vaccines(
    vtype VARCHAR(100) NOT NULL PRIMARY KEY,
    vname VARCHAR(100) NOT NULL,
    dose INT NOT NULL, --1st dose or 2nd dose?
    avail_num INT
);

CREATE TABLE Locations(
    locid INT NOT NULL IDENTITY PRIMARY KEY,
    locname VARCHAR(100) NOT NULL,
    locaddress VARCHAR(500) NOT NULL
);

CREATE TABLE CareGiverSchedule(
    schid INT NOT NULL IDENTITY PRIMARY KEY,
    cgid INT FOREIGN KEY REFERENCES Caregivers(cgid),
    availdate DATE,
    starttime TIME,
    endtime TIME,
    bookStatus VARCHAR(30)
);

CREATE TABLE Appointment(
    apptid INT NOT NULL IDENTITY PRIMARY KEY,
    pid INT FOREIGN KEY REFERENCES Patients(pid),
    vtype VARCHAR(100) FOREIGN KEY REFERENCES Vaccines(vtype),
    locid INT FOREIGN KEY REFERENCES Locations(locid),
    cgid INT FOREIGN KEY REFERENCES Caregivers(cgid),
    apptdate DATE NOT NULL,
    appttime TIME NOT NULL,
    dose_num INT NOT NULL,  --1st or 2nd does?
    appt_status INT  --1 = show, 0 = no show
);

EXEC InitDataModel;

--For cleaning purpose--
CREATE PROCEDURE DropInitDataModel
AS
DROP TABLE Appointment;
DROP TABLE CareGiverSchedule;
DROP TABLE Caregivers;
DROP TABLE Locations;
DROP TABLE Patients;
DROP TABLE Vaccines;

EXEC DropInitDataModel


INSERT INTO Caregivers VALUES ('Jane');
INSERT INTO Caregivers VALUES ('Abby');
INSERT INTO Caregivers VALUES ('Tom');
INSERT INTO Caregivers VALUES ('Amy');
INSERT INTO Caregivers VALUES ('Blake');

INSERT INTO Locations VALUES ('Location1', '1st st location');
INSERT INTO Locations VALUES ('Location2', '2nd st location');
INSERT INTO Locations VALUES ('Location3', '3rd st location');
INSERT INTO Locations VALUES ('Location4', '4th st location');
INSERT INTO Locations VALUES ('Location1', '5th st location');

INSERT INTO Patients VALUES ('Emma', '1998-01-05', 'Teacher');
INSERT INTO Patients VALUES ('Jeremy', '1998-01-10', 'Engineer');
INSERT INTO Patients VALUES ('Alex', '1990-05-05', 'Sales');
INSERT INTO Patients VALUES ('Cloe', '1978-07-25', 'Student');
INSERT INTO Patients VALUES ('Lily', '1965-11-05', 'Retired');

INSERT INTO Vaccines VALUES ('Pfizer1', 'Pfizer Tech', 1, 100);
INSERT INTO Vaccines VALUES ('Pfizer2', 'Pfizer Tech', 2, 100);
INSERT INTO Vaccines VALUES ('Moderna1', 'Moderna Tech', 1, 100);
INSERT INTO Vaccines VALUES ('Moderna2', 'Moderna Tech', 2, 100);
INSERT INTO Vaccines VALUES ('JJ', 'Johnson&Johnson', 1, 150);

INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '09:00:00', '09:15:00', 'Booked');
INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '09:15:00', '09:30:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '09:30:00', '09:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '09:45:00', '10:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '10:00:00', '10:15:00', 'Booked');
INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '10:15:00', '10:30:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '10:30:00', '10:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (1, '2021-05-10', '10:45:00', '11:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '09:00:00', '09:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '09:15:00', '09:30:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '09:30:00', '09:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '09:45:00', '10:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '10:00:00', '10:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '10:15:00', '10:30:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '10:30:00', '10:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (2, '2021-05-10', '10:45:00', '11:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:00:00', '11:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:15:00', '11:30:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:30:00', '11:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:45:00', '12:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:00:00', '11:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:15:00', '11:30:00', 'Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:30:00', '11:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (3, '2021-05-10', '11:45:00', '12:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:00:00', '11:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:15:00', '11:30:00', 'Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:30:00', '11:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:45:00', '12:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:00:00', '11:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:15:00', '11:30:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:30:00', '11:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (4, '2021-05-10', '11:45:00', '12:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '12:00:00', '12:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '12:15:00', '12:30:00', 'Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '12:30:00', '12:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '12:45:00', '13:00:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '13:00:00', '13:15:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '13:15:00', '13:30:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '13:30:00', '13:45:00', 'Not Booked');
INSERT INTO CareGiverSchedule VALUES (5, '2021-05-10', '13:45:00', '14:00:00', 'Not Booked');

INSERT INTO Appointment VALUES(1, 'Pfizer1', 5, 5, '2021-05-10', '12:15:00', 1, 1)
INSERT INTO Appointment VALUES(2, 'Moderna1', 3, 4, '2021-05-10', '11:15:00', 1, 1)
INSERT INTO Appointment VALUES(3, 'Pfizer2', 2, 3, '2021-05-10', '11:15:00', 2, 1)
INSERT INTO Appointment VALUES(4, 'Moderna1', 1, 1, '2021-05-10', '09:00:00', 1, 1)
INSERT INTO Appointment VALUES(5, 'JJ', 1, 1, '2021-05-10', '10:00:00', 1, 1)

SELECT avail_num
FROM Vaccines
WHERE
dose = 2 AND vtype = 'Pfizer2'
