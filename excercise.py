import pandas as pd
import datetime
import time
import soundEffects as sound
import sys
import os
import mysql.connector
import select
from pynput import keyboard

class Trainingsplan: 
    def __init__(self):
        self.pauseLength = 0
        self.begin = None
        self.end = None
        self.excercises = []

    def result(self):
        return None

    def addExcercise(self, name="Exercise", maxReps=10, sets=4, up=3, down=3):
        excercise = Excercise(name=name)
        for i in range(sets):
            excercise.addSet(name=excercise.name + "." + str(i + 1), maxReps=maxReps, up=up, down=down)
        self.excercises.append(excercise)

    def startTraining(self, pauseDuration=60, warmup=True):
        os.system('clear')
        self.begin = pd.Timestamp(datetime.datetime.now())
        print("Training started at " + str(self.begin))
        for excercise in self.excercises:
            excercise.startExcercise(pauseDuration)
        self.end = pd.Timestamp(datetime.datetime.now())

    def printResult(self):
        os.system('clear')
        for excercise in self.excercises:
            print(excercise.name + ": ", end="\n")
            print("  From " + str(excercise.beginn) + " to " + str(excercise.end))
            print("  Positive phase: " + str(excercise.up) + "s. Negative phase: " + str(excercise.down) + "s.")
            print("  Exercise performance: ", end="")
            for set in excercise.sets:
                print(str(set.doneReps) + "/" + str(set.maxReps), end=" ")
            print()

    def saveResult(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="trainingsuser",
            passwd="123456",
            database="training"
        )

        mycursor = mydb.cursor()

        # Add training
        sqlquery = "INSERT INTO training (startTime, endTime) VALUES (TIMESTAMP(%s), TIMESTAMP(%s));"
        mycursor.execute(sqlquery, (self.begin, self.end))
        trainingId = mycursor.lastrowid
        mydb.commit()

        mycursor.execute("SELECT * FROM training")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
        
        # Add exercises
        for excercise in self.excercises:
            sqlquery = """
                INSERT INTO exercises (name, startTime, endTime, pauseLength, upLength, downLength, trainingId)
                VALUES (%s, TIMESTAMP(%s), TIMESTAMP(%s), %s, %s, %s, %s)
            """
            mycursor.execute(sqlquery, (
                excercise.name, excercise.beginn, excercise.end,
                excercise.pause, excercise.up, excercise.down, trainingId
            ))
            excerciseId = mycursor.lastrowid
            mydb.commit()

            for set in excercise.sets:
                sqlquery = """
                    INSERT INTO sets (exerciseId, doneReps, plannedReps)
                    VALUES (%s, %s, %s)
                """
                mycursor.execute(sqlquery, (excerciseId, set.doneReps, set.maxReps))
                mydb.commit()


class Excercise:
    def __init__(self, name="Exercise"):
        self.name = name
        self.beginn = None
        self.end = None
        self.pause = None
        self.sets = []
        self.up = 0
        self.down = 0

    def addSet(self, name="Exercise", maxReps=10, up=3, down=3):
        self.up = up
        self.down = down
        set = Set(name=name, maxReps=maxReps, up=up, down=down)
        self.sets.append(set)
        
    def startExcercise(self, pauseDuration=60):
        self.pause = pauseDuration
        self.beginn = pd.Timestamp(datetime.datetime.now())
        print("Starting " + self.name)
        for i in range(len(self.sets)):
            self.sets[i].playSet()
            pause(pauseDuration)
        self.end = pd.Timestamp(datetime.datetime.now())

class Set:
    def __init__(self, name="Exercise", maxReps=10, up=3, down=3):
        self.name = name
        self.maxReps = maxReps
        self.doneReps = 0
        self.up = up
        self.down = down

    def playSet(self):
        rep = 0
        while rep < self.maxReps:
            os.system('clear')
            print(self.name)
            print(str(rep + 1) + " of " + str(self.maxReps))
            print(" ")
            print(" ")
            print(" ")
            print("Press ENTER to abort set")
            self.doneReps = rep + 1
            sound.playSound(self.up + self.down)
            rep += 1
            if self.detect_key_press():
                break

    def detect_key_press(self):
        """Detects key press and returns True if ENTER is pressed"""
        def on_press(key):
            try:
                if key == keyboard.Key.enter:
                    return False  # Stop listener
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join(timeout=0.1)  # Timeout in seconds
        return False


def pause(length):
    os.system('clear')
    print("Well done... Now rest for " + str(length) + " seconds!")
    for j in range(length):
        if j == length - 10:
            sound.playEffect("gong")
        os.system('clear')
        timeLeft = length - j  # Gong 10 seconds before pause ends
        print("Time until training continues: " + str(timeLeft))
        time.sleep(1)

# Test scenario
if __name__ == "__main__":
    training = Trainingsplan()
    training.addExcercise(name="Pushups", maxReps=8, sets=3, up=3, down=3)
    training.addExcercise(name="Situps", maxReps=8, sets=3, up=3, down=3)
    training.addExcercise(name="Planks", maxReps=8, sets=3, up=3, down=3)
    training.addExcercise(name="Rückenzieher", maxReps=8, sets=3, up=3, down=3)
    training.addExcercise(name="Kniebeugen", maxReps=10, sets=3, up=3, down=3)
    training.startTraining(pauseDuration=60)
    training.printResult()
    training.saveResult()
    time.sleep(10)