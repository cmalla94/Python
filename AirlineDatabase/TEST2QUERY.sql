--TEST QUERY 

--CREATE PERSON AND ASSOCIATION TABLE AND ASSOCIATE THEM WITH FOREIGN KEY 
CREATE TABLE Person(
	p_id	INTEGER, 
	age		INTEGER,
	PRIMARY KEY(p_id))

CREATE TABLE Association(
	p_id	INTEGER,
	a_id	INTEGER,
	e_id	INTEGER, 
	FOREIGN KEY (e_id) REFERENCES Exercise,
	FOREIGN KEY (p_id) REFERENCES Person,
	PRIMARY KEY (p_id , a_id , e_id)) 


CREATE TABLE Exercise(
	e_id	INTEGER,
	calories INTEGER,
	PRIMARY KEY (e_id))

CREATE FUNCTION numOfRows(@x INTEGER)
	RETURNS INTEGER
	AS 
	BEGIN
		DECLARE	@result INTEGER;
		SELECT	@result = COUNT(*)
		FROM	(SELECT A.p_id
				FROM	Assocation A
				WHERE	A.p_id = @x) A
		RETURN	@result
	END;

--CREATE TRIGGER THAT DOESN'T DELETION OF PERSON THAT HAS AN ASSOCIATION 
DROP TRIGGER DeletedPersonTrigger;

CREATE TRIGGER	DeletedPersonTrigger
ON	Person
INSTEAD OF DELETE
AS 
BEGIN
	DECLARE @result INTEGER;
	SELECT @result = 
	(SELECT COUNT(*) FROM (deleted d INNER JOIN Association A ON d.p_id = A.p_id))

	IF @result > 0
		PRINT @result;

	ELSE IF @result = 0
		DELETE FROM Person 
		WHERE p_id IN (SELECT d.p_id FROM deleted d);
END
					
		
		

		
		
		 
		
INSERT INTO Person
SELECT '1' , '20' UNION
SELECT '2' , '20' UNION 
SELECT '3' , '30' UNION 
SELECT '4' , '25';

INSERT INTO Assocation
SELECT	'1' , '1' UNION
SELECT	'1' , '2' UNION
SELECT	'4' , '1' UNION
SELECT	'4' , '3';


--TEST TO DELETE PERSON 1 

DELETE FROM Person 
WHERE	p_id IN (2 ,  3);

INSERT INTO Person
SELECT '2' , '20' UNION 
SELECT '3' , '30'

SELECT * FROM Person
SELECT * FROM Assocation

--TESTING FOR MILES UPDATE TRIGGER
DROP TRIGGER whatActionTrigger;

CREATE TRIGGER whatActionTrigger
ON Person 
AFTER INSERT, UPDATE, DELETE 
AS 
BEGIN
	IF (EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted))
		BEGIN PRINT 'UPDATE' END

	ELSE IF (EXISTS (SELECT * FROM inserted) AND NOT EXISTS (SELECT * FROM deleted))
		BEGIN PRINT 'INSERTED' END

	ELSE IF (NOT EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted))
		BEGIN PRINT 'DELETED' END

END

CREATE TRIGGER	weightUpdateTrigger
ON Association 
AFTER INSERT, UPDATE, DELETE
AS 
BEGIN
	IF (EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted))
		BEGIN 
			DECLARE @oldcalories INTEGER;
			DECLARE @newcalories INTEGER;
			DECLARE @p_id	INTEGER;

			SELECT @oldcalories = (SELECT E.calories FROM
				(deleted d INNER JOIN Exercise E ON d.e_id = E.e_id))
			SELECT @newcalories = (SELECT E.calories FROM
				(inserted i INNER JOIN Exercise E ON i.e_id = E.e_id))
			SELECT @p_id = i.p_id FROM inserted i;

			UPDATE Person
			SET	weight = ((weight - @oldcalories) + @newcalories)
			WHERE p_id = @p_id;
		END
	ELSE IF (EXISTS (SELECT * FROM inserted) AND NOT EXISTS (SELECT * FROM deleted))
		BEGIN 
			DECLARE @calories INTEGER;

			SELECT @calories = (SELECT E.calories FROM 
				(inserted i INNER JOIN Exercise E ON i.e_id = E.e_id))
			SELECT @p_id = i.p_id FROM inserted i;

		UPDATE Person
		SET	weight = weight + @calories
		WHERE p_id = @p_id;

		END

	ELSE IF (NOT EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted))
		BEGIN 
			SELECT @calories = (SELECT E.calories FROM
				(deleted d INNER JOIN Exercise E ON d.e_id = E.e_id));
			SELECT @p_id = d.p_id FROM deleted d;

			UPDATE Person 
			SET weight = weight - @calories
			WHERE p_id = @p_id;
		END
END

DELETE FROM Person;
DELETE FROM Association;
DELETE FROM Exercise;

SELECT * FROM Person; SELECT * FROM Association; SELECT * FROM Exercise;

INSERT INTO Exercise
SELECT '1','120' UNION
SELECT '2','50' UNION
SELECT '3','200';

INSERT INTO Person
SELECT '1','14','0' UNION
SELECT '2','16','0' UNION
SELECT '3','20','0';

SELECT * FROM Person; SELECT * FROM Association; SELECT * FROM Exercise;

INSERT INTO Association
SELECT '1','1','1';
INSERT INTO Association
SELECT '2','2','2';
INSERT INTO Association
SELECT '3','3','3';

SELECT * FROM Person; SELECT * FROM Association; SELECT * FROM Exercise;

UPDATE Association
SET e_id = '2'
WHERE p_id = '1';

SELECT * FROM Person; SELECT * FROM Association; SELECT * FROM Exercise;

INSERT INTO Association
SELECT '1','1','3';

DELETE FROM Association
WHERE p_id = '1' AND a_id = '1' AND e_id = '2';

INSERT INTO Airport 
SELECT '001', 'Toronto Airport', 'Vancouver' UNION
SELECT '010', 'England Airport', 'Hyderbad';

INSERT INTO Flight
SELECT '000001', '100', 'yvr', 'hyd';

INSERT INTO Flight_Instance
SELECT '000001', '20161203', '001', '2';

INSERT INTO Passenger 
SELECT '2', 'John', 'Smith', '0';

DELETE FROM Airport
DELETE FROM Flight
DELETE FROM Flight_Instance
DELETE FROM Passenger

SELECT * FROM Airport; SELECT * FROM Flight; SELECT * FROM Flight_Instance; SELECT * FROM Passenger
SELECT COUNT(*) FROM Passenger WHERE passenger_id = 1;

SELECT COUNT(*) FROM Flight WHERE flight_code = abcdef;

SELECT * FROM Flight_Instance;

SELECT * FROM Flies WHERE flight_code = 'abcdef';

DELETE FROM Flies

CREATE VIEW PersonView AS SELECT p_id FROM Person;

SELECT * FROM PassengerView

CREATE VIEW PassengerView AS SELECT * FROM Passenger) 
SELECT	DISTINCT P.passenger_id, P.first_name, P.last_name,P.miles, F.flight_code, F.departs, F2.distance, D.airport_name, A.airport_name
FROM	Passenger P, (Flies F INNER JOIN Flight F2 ON F.flight_code = F2.flight_code),
		(Flight F3 INNER JOIN Airport D ON F3.departure_iata = D.iata),
		(Flight F4 INNER JOIN Airport A ON F4.arrival_iata = A.iata)) 
SELECT * FROM Flies