import mysql.connector
from mysql.connector import Error
import datetime
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="my-secret-pw",
  database="training",
  port = 3306
)


mycursor = mydb.cursor()

start = pd.Timestamp(datetime.datetime.now())
end = pd.Timestamp(datetime.datetime.now())


sqlquery = "INSERT INTO training (startTime,endTime) VALUES (TIMESTAMP('"+str(start)+"'),TIMESTAMP('2002-02-02'));"                

mycursor.execute(sqlquery)

##mycursor.execute("DELETE FROM training")

#mycursor.execute("INSERT INTO excercises (excerciseId,doneReps,plannedReps) VALUES (1,4,10);")
#mycursor.execute("INSERT INTO sets (excerciseId,doneReps,plannedReps) VALUES (1,4,10);")

#mycursor.execute("SELECT * FROM training")

#myresult = mycursor.fetchall()

mydb.commit()

mycursor.execute("select * from training")

myresult = mycursor.fetchall();


for x in myresult:
  print(x)


#print("1 record inserted, ID:", mycursor.lastrowid)