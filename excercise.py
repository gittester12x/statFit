import pandas as pd
import datetime 
import time
import soundEffects as sound
import sys


class Trainingsplan: 
    pauseLength = 0
    beginn = None
    end = None
    excercises = []

    def result(self):
        return None

    def addExcercise(self):
        excercise = Excercise()
        excercise.addSet(Pushup(10,3,3))
        excercise.addSet(Pushup(10,3,3))
        excercise.addSet(Pushup(10,3,3))
        excercise.addSet(Pushup(10,3,3))

        self.excercises.append(Excercise())

    def startTraining(self):
        beginn = pd.Timestamp(datetime.datetime.now())
        print("Training started at "+str(beginn))
        for excercise in self.excercises:
            excercise.startExcercise()
            pause(90)

class Excercise:
    name = " "
    beginn = None
    end = None
    pause = None
    sets = []

    def addSet(self,set):
        self.sets.append(set)

    def startExcercise(self):
        for set in self.sets:
            set.playSet()

class Set:
    def __init__(self,maxReps = 10):
        self.maxReps = maxReps
        self.doneReps = 0
    def playSet(self):
        time.sleep(1)


class Pushup(Set):
    def __init__(self,maxReps = 10,up = 3,down = 3):
        self.maxReps = maxReps
        self.doneReps = 0
        self.up = up
        self.down = down

    def playSet(self):
        for rep in range(self.maxReps):
            sound.playSound(self.up+self.down)
        
    def getResult(self):
        print("\nSo... how many pushups did you make?")
        self.doneReps = input()
            


def pause(length):
    print("\nWell done... Now rest for a minute!\n")
    for j in range(length):
        sys.stdout.write('\r\a{j}'.format(j=length-j))
        sys.stdout.flush()
        time.sleep(1)
