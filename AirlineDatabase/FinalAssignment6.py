import pymssql #import python ms sql library
from datetime import datetime

def strToDate(ymd):
    return datetime.date(*map(int, ymd.split('-')))

conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_cmalla', password='e4aREa7FHY6742n7', database='cmalla354')
cursor = conn.cursor()

pid = raw_input("ENTER THE PASSENGER ID: ")
flight = raw_input("ENTTER THE FLIGHT CODE: ")
year = raw_input("ENTER THE DEPARTURE YEAR , YYYY ")
month = raw_input("ENTER THE DEPARTURE MONTH , MM ")
day = raw_input("ENTER THE DEPARTURE DAY , DD ")
departs = year + '-' + month + '-' + day
#CHAD MALLA
#301220878
#CMPT354 ASSIGNMENT 6



print('%s' %departs)
cursor.execute('SELECT COUNT(*) FROM Passenger WHERE passenger_id = %s' % (pid))
count1 = cursor.fetchone()


cursor.execute("SELECT COUNT(*) FROM Flight_Instance WHERE flight_code = '%s'" % flight)
count2 = cursor.fetchone()


cursor.execute("SELECT COUNT(*) FROM Flight_Instance WHERE departs = '%s'" % datetime.strptime(str(departs), '%Y-%m-%d'))
count3 = cursor.fetchone()

departs = str(year + month + day)
#cursor.execute("INSERT INTO Flies VALUES ('abcdef' , '20161202' , '1')")
print("%s" %departs)
if((count1 > 0) and (count2 > 0) and (count3 > 0)):
    cursor.execute("INSERT INTO Flies VALUES ('%s' ,'%s',%d)"  % (flight, str(departs), int(pid)))
conn.commit()

cursor.execute("SELECT * FROM Passenger WHERE passenger_id = %s" % (pid))
row = cursor.fetchone()
while row:
    print("ID = %s, First Name = %s, Last Name = %s, miles = %s" % (row[0], row[1], row[2], row[3]))
    row = cursor.fetchone()

cursor.execute("""SELECT DISTINCT F.flight_code, F.departs, F2.distance, D.airport_name, A.airport_name AS arrival
FROM (Flies F INNER JOIN Flight F2 ON F.flight_code = F2.flight_code),(Flight F3 INNER JOIN Airport D ON F3.departure_iata = D.iata),
(Flight F4 INNER JOIN Airport A ON F4.arrival_iata = A.iata) WHERE F.passenger_id = %s""" % (pid))

row = cursor.fetchone()
while row:
    print("flight_code = %s, departure date = %s, distance = %s, departure airport = %s, arrival airport = %s" % (row[0], row[1], row[2], row[3], row[4]))
    row = cursor.fetchone()
conn.close()

