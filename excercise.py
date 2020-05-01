import pandas as pd
import datetime 
import time
import soundEffects as sound
import sys
import os
import keyboard  # using module keyboard
import select 
import mysql.connector

class Trainingsplan: 
    pauseLength = 0
    begin = None
    end = None
    excercises = []

    def result(self):
        return None

    def addExcercise(self,name = "Excercise", maxReps=10,sets = 4, up = 3, down = 3):
        excercise = Excercise(name=name)
        for i in range(sets):
            excercise.addSet(name=excercise.name+"."+excercise.name,maxReps=10,up=up,down=down)
        self.excercises.append(excercise)

    def startTraining(self,pauseDuration = 60,warmup = True):
        os.system('clear')
        self.begin = pd.Timestamp(datetime.datetime.now())
        print("Training started at "+str(self.begin))
        for excercise in self.excercises:
            excercise.startExcercise(pauseDuration)
        self.end = pd.Timestamp(datetime.datetime.now())

    def printResult(self):
        os.system('clear')
        for excercise in self.excercises:
            print(excercise.name+": ",end="\n")
            print("  From "+str(excercise.beginn)+" to "+str(excercise.end))
            print("  Positive phase: "+str(excercise.up)+"s. Negative phase: "+str(excercise.down)+"s.")
            print("  Excercise performance: ",end="")
            for set in excercise.sets:
                print(str(set.doneReps)+"/"+str(set.maxReps),end=" ")
            print()

    def saveResult(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="trainingsuser",
        passwd="123456",
        database="training"
        )

        mycursor = mydb.cursor()

        ## add training
        sqlquery = "INSERT INTO training (startTime,endTime) VALUES (TIMESTAMP('"+str(self.begin)+"'),TIMESTAMP('"+str(self.end)+"'));"                
        mycursor.execute(sqlquery)
        trainingId = mycursor.lastrowid
        mydb.commit()

        mycursor.execute("select * from training")

        myresult = mycursor.fetchall();
        for x in myresult:
            print(x)
        
        ##add excerrcises
        for excercise in self.excercises:
            sqlquery = "INSERT INTO excercises "
            sqlquery += "(name,startTime,endTime,pauseLength,upLength,downLength,trainingId)"
            sqlquery += " VALUES ("
            sqlquery += "'"+excercise.name+"'"+","
            sqlquery += "TIMESTAMP('"+str(excercise.beginn)+"'),"
            sqlquery += "TIMESTAMP('"+str(excercise.end)+"'),"
            sqlquery += str(excercise.pause)+","
            sqlquery += str(excercise.up)+","
            sqlquery += str(excercise.down)+","
            sqlquery += str(trainingId)+")"

            
            mycursor.execute(sqlquery)
            excerciseId = mycursor.lastrowid

            mydb.commit()

            for set in excercise.sets:
                sqlquery = "INSERT INTO sets "
                sqlquery += "(excerciseId,doneReps,plannedReps)"
                sqlquery += " VALUES ("
                sqlquery += str(excerciseId)+","
                sqlquery += str(set.doneReps)+","
                sqlquery += str(set.maxReps)+")"

                print(sqlquery)
                mycursor.execute(sqlquery)
                mydb.commit()










class Excercise:
    def __init__(self,name = "Excercise"):
        self.name = name
        self.beginn = None
        self.end = None
        self.pause = None
        self.sets = []
        self.up = 0
        self.down = 0

    def addSet(self,name = "Excercise",maxReps = 10, up = 3, down = 3):
        self.up = up
        self.down = down
        set = Set(name = name,maxReps = 10, up = 3, down = 3)
        self.sets.append(set)
        

    def startExcercise(self,pauseDuration = 60):
        self.pause=pauseDuration
        self.beginn = pd.Timestamp(datetime.datetime.now())
        print("Starting  "+self.name)
        for i in range(len(self.sets)):
            self.sets[i].playSet()
            pause(pauseDuration)
        self.end = pd.Timestamp(datetime.datetime.now())
            
class Set:
    def __init__(self,name = "Excercise",maxReps = 10, up = 3, down = 3):
        self.name = name
        self.maxReps = maxReps
        self.doneReps = 0
        self.up = up
        self.down = down

    def playSet(self):
        while True:    
            for rep in range(self.maxReps):
                i,o,e = select.select([sys.stdin],[],[],0.0001)
                if i == [sys.stdin]:
                    strangeThing = sys.stdin.readline().strip()
                    break
                os.system('clear')
                print(self.name)
                print(str(rep+1)+" of "+str(self.maxReps))
                ##print(rep+1)
                print(" ")
                print(" ")
                print(" ")
                print("Press ENTER to abort set")
                self.doneReps=rep+1
                sound.playSound(self.up+self.down)
            break   

        ### Deprecated
        ##self.getResult()



        

def pause(length):
    os.system('clear')
    print("Well done... Now rest for "+str(length)+" seconds!")
    for j in range(length):
        if j==length-10:
            sound.playEffect("gong")
        os.system('clear')
        timeLeft = length-j                                ## Gong 10 seconds before pause ends
        print("Time until training continues: "+str(timeLeft))
        time.sleep(1)


### Testscenario
if __name__ == "__main__":
    training = Trainingsplan()
    training.addExcercise(name = "Pushups", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Situps", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Planks", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Rückenzieher", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Kniebeugen links", maxReps = 10, sets = 3, up = 3, down = 3)
    training.addExcercise(name = "Kniebeugen rechts", maxReps = 10, sets = 3, up = 3, down = 3)
    training.startTraining(pauseDuration=90)
    training.printResult()
    training.saveResult();
    time.sleep(10)

