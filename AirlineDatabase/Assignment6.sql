

--Create Airport Table

CREATE TABLE Airport(
	iata	CHAR(3),
	airport_name	CHAR(30) NOT NULL, 
	city	CHAR(20) NOT NULL,
	PRIMARY KEY (iata), 
	UNIQUE (airport_name))

--Create Flight Table 

CREATE TABLE Flight(
	flight_code	CHAR(6),
	distance	INTEGER NOT NULL, 
	departure_iata CHAR(3) NOT NULL,
	arrival_iata CHAR(3) NOT NULL, 
	PRIMARY KEY (flight_code), 
	FOREIGN KEY (departure_iata) REFERENCES Airport,
	FOREIGN KEY (arrival_iata) REFERENCES Airport,
	CHECK (departure_iata <> arrival_iata)) --Checking that the departure airport and arrival are different 

--Create Flight Instance Table 

CREATE TABLE Flight_Instance(
	flight_code	CHAR(6), 
	departs	DATE,
	gate	CHAR(3), 
	aircraft_id	TINYINT,
	PRIMARY KEY (flight_code , departs),
	FOREIGN KEY (flight_code) REFERENCES Flight ON DELETE CASCADE 
	ON UPDATE CASCADE,
	CONSTRAINT once_a_day UNIQUE (departs , aircraft_id)) --aircraft can only fly once per day 

--Create Passenger Table 

CREATE TABLE Passenger(
	passenger_id	INTEGER, 
	first_name	CHAR(20) NOT NULL,
	last_name	CHAR(20) NOT NULL, 
	miles	INTEGER NOT NULL, 
	PRIMARY KEY (passenger_id))

--Create Flies Table 

CREATE TABLE Flies(
	flight_code	CHAR(6),
	departs	DATE,
	passenger_id	INTEGER,
	PRIMARY KEY (flight_code, departs, passenger_id), 
	FOREIGN KEY (flight_code, departs) REFERENCES Flight_Instance ON UPDATE CASCADE, 
	FOREIGN KEY (passenger_id) REFERENCES Passenger)

	
--Trigger to stop deleting passenger that have associate Flies records

CREATE TRIGGER DeletedPassengerTrigger
ON Passenger
INSTEAD OF DELETE
AS
BEGIN
	SET NOCOUNT ON;
	DECLARE @result INTEGER;
	SELECT @result =  (SELECT COUNT(*)
		FROM	(deleted D INNER JOIN Flies F ON
		D.passenger_id = F.passenger_id)) 

	IF (@result > 0)
		PRINT @result;
	ELSE IF (@result = 0)
		DELETE FROM Passenger  
		WHERE passenger_id IN (SELECT d.passenger_id FROM deleted d);
END

--Trigger to update the miles every time passenger flies
--updates the miles attribute of the passenger table
--when records of the Files table are inserted, deleted or updated
--use after trigger 
CREATE TRIGGER MilesUpdateTrigger
--triggers when changes happen to Flies table
ON Flies
AFTER INSERT, DELETE, UPDATE
AS
BEGIN 
	SET NOCOUNT ON;

	--CASE IF ACTION = UPDATE
	IF (EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted))
		BEGIN
			DECLARE @oldmiles INTEGER;
			DECLARE @newmiles INTEGER;
			DECLARE @passenger_id INTEGER;

			SELECT @oldmiles = (SELECT F.distance FROM
						(deleted d INNER JOIN Flight F ON d.flight_code = F.flight_code))
			SELECT @newmiles = (SELECT F.distance FROM 
						(inserted i INNER JOIN Flight F ON i.flight_code = F.flight_code))
			SELECT @passenger_id = i.passenger_id FROM inserted i;
			UPDATE	Passenger
			SET		miles = ((miles - @oldmiles) + @newmiles)
			WHERE	passenger_id = @passenger_id;
		END

	
	--CASE IF ACTION = INSERT
	ELSE IF (EXISTS (SELECT * FROM inserted) AND NOT EXISTS (SELECT * FROM deleted))
		BEGIN
			DECLARE @miles INTEGER;
			
			SELECT	@miles = (SELECT F.distance FROM
					(inserted i INNER JOIN Flight F ON i.flight_code = F.flight_code));
			SELECT	@passenger_id = i.passenger_id FROM inserted i;

			UPDATE	Passenger
			SET		miles = (miles + @miles)
			WHERE	passenger_id = @passenger_id;
		END


	--CASE IF ACTION = DELETE
	ELSE IF (EXISTS (SELECT * FROM deleted) AND NOT EXISTS (SELECT * FROM inserted))
		BEGIN 
			SELECT @miles = (SELECT F.distance FROM
					(deleted d INNER JOIN Flight F ON d.flight_code = F.flight_code));
			SELECT @passenger_id = d.passenger_id FROM deleted d;

			UPDATE	Passenger 
			SET		miles = (miles - @miles)
			WHERE	passenger_id = @passenger_id;
		END
END


