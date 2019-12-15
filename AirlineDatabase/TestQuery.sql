--Want to test if aircraft only flies once a day 

CREATE TABLE Flight_Instance_T( 
	Flight_Code_T CHAR(3),
	departs_T	DATE,
	gate_T	CHAR(3), 
	aircraft_id_T	TINYINT,
	PRIMARY KEY (Flight_Code_T, departs_T),
	CONSTRAINT once_a_day UNIQUE (departs_T , aircraft_id_T)) --aircraft can only fly once per day



INSERT INTO Flight_Instance_T
--SELECT 'JA1', '11/28/16' , 'D9' , 6 UNION
--SELECT 'JA2', '11/28/16' , 'D8' , 8 UNION
--SELECT 'JA3', '11/28/16' , 'D8' , 6;
SELECT 'JA3', '11/19/16', 'D8' , 6; 

--Testing that dept and arrival can't be same for one Flight object 

CREATE TABLE Flight_T(
	flight_code_T	CHAR(6),
	distance_T	INTEGER NOT NULL, 
	departure_iata_T CHAR(3) NOT NULL,
	arrival_iata_T CHAR(3) NOT NULL, 
	PRIMARY KEY (flight_code_T), 
	CHECK (departure_iata_T <> arrival_iata_T))

INSERT INTO Flight_T
--SELECT 'JA1', '111', 'ABC' , 'AAC' UNION 
--SELECT 'JA2', '111', 'ABC' , 'AAC' UNION 
SELECT 'JA3', '111', 'ABC' , 'ABC'

--Output the two tables 

SELECT * FROM Flight_T
SELECT * FROM Flight_Instance_T

--Testing how to output information as a trigger action

CREATE TRIGGER
output_just_ins
ON Flight_T
AFTER INSERT 
AS
	declare @flight_code_T CHAR(6);
	declare @distance_T INTEGER;
	declare @departure_iata_T CHAR(3);
	declare @arrival_iata_T CHAR(3);	
		
	SELECT @flight_code_T = i.flight_code_T FROM inserted i;
	SELECT @distance_T =  i.distance_T FROM inserted i;
	SELECT @departure_iata_T = i.departure_iata_T FROM inserted i;
	SELECT @arrival_iata_T = i.arrival_iata_T FROM inserted i;

	PRINT @flight_code_T + ',' + @departure_iata_T; 

INSERT INTO Flight_T
SELECT 'JA5', '112', 'ABL' , 'ABH'

--Trying to implement a function that returns number of rows where colID = x?

CREATE FUNCTION numOfRec3 
(@x CHAR(3))
RETURNS INTEGER
AS
BEGIN

DECLARE @NumofRows INTEGER
SELECT @NumofRows = COUNT(*)
FROM(
	SELECT flight_code_T 
	FROM Flight_T
	WHERE departure_iata_T = @x) A
RETURN @NumofRows
END

CREATE TRIGGER whatIstheNumOFRecWithflightcodeX1
ON Flight_T
AFTER INSERT 
AS
	declare @x CHAR(6)
	SELECT @x = i.departure_iata_T FROM inserted i;

	declare @result INTEGER

	SELECT @result = dbo.numOfRec3(@x)

	PRINT @result

SELECT	F.flight_code_T
FROM	Flight_T F

INSERT INTO Flight_T
SELECT 'JB9', '111', 'ABC' , 'AOO' 