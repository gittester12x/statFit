import pandas as pd
import datetime 
import time
import soundEffects as sound
import sys
import os
import keyboard  # using module keyboard

class Trainingsplan: 
    pauseLength = 0
    beginn = None
    end = None
    excercises = []

    def result(self):
        return None

    def addExcercise(self,name = "Excercise", maxReps=10,sets = 4, up = 3, down = 3):
        excercise = Excercise(name=name)
        for i in range(sets):
            excercise.addSet(name=name,maxReps=10,up=up,down=down)
        self.excercises.append(excercise)

    def startTraining(self,pauseDuration = 60,warmup = True):
        os.system('clear')
        beginn = pd.Timestamp(datetime.datetime.now())
        print("Training started at "+str(beginn))
        for excercise in self.excercises:
            excercise.startExcercise(pauseDuration)
        end = pd.Timestamp(datetime.datetime.now())
            

class Excercise:
    def __init__(self,name = "Excercise"):
        self.name = name
    beginn = None
    end = None
    pause = None
    sets = []

    def addSet(self,name = "Excercise",maxReps = 10, up = 3, down = 3):
        self.sets.append(Set(name = self.name,maxReps = 10, up = 3, down = 3))
        

    def startExcercise(self,pauseDuration = 60):
        print("Starting  "+self.name)
        for i in range(len(self.sets)):
            self.sets[i].playSet()
            pause(pauseDuration)
            
            
class Set:
    def __init__(self,name = "Excercise",maxReps = 10, up = 3, down = 3):
        self.name = name
        self.maxReps = maxReps
        self.doneReps = 0
        self.up = up
        self.down = down

    def playSet(self):
        while True:
            try:
                if keyboard.is_pressed('space')
        for rep in range(self.maxReps):
            os.system('clear')
            print("Excercise: "+self.name)
            print(rep+1)
            
            sound.playSound(self.up+self.down)
        self.getResult()
    
    def getResult(self):
        print("So... how many pushups did you make?")
        self.doneReps = input()


### deprecated
class Pushup(Set):
    def __init__(self,maxReps = 10,up = 3,down = 3):
        self.maxReps = maxReps
        self.doneReps = 0
        self.up = up
        self.down = down

    def getResult(self):
        print("So... how many pushups did you make?")
        self.doneReps = input()

    def playSet(self):
        for rep in range(self.maxReps):
            os.system('clear')
            print("Excercise: ")
            print(rep)
            sound.playSound(self.up+self.down)
        self.getResult()
        

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
    pause(60)
    training = Trainingsplan()
    training.addExcercise(name = "Pushups", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Situps", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Planks", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Rückenzieher", maxReps = 10, sets = 4, up = 3, down = 3)
    training.addExcercise(name = "Kniebeugen links", maxReps = 10, sets = 3, up = 3, down = 3)
    training.addExcercise(name = "Kniebeugen rechts", maxReps = 10, sets = 3, up = 3, down = 3)
    training.startTraining(pauseDuration=60)
