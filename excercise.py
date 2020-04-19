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
            

class Excercise:
    name = " "
    beginn = None
    end = None
    pause = None
    sets = []

    def addSet(self,set):
        self.sets.append(set)

    def startExcercise(self,pauseDuration = 60):
        for i in range(len(self.sets)):
            self.sets[i].playSet()
            pause(pauseDuration)
            
class Set:
    def __init__(self,name = "Excercise",maxReps = 10, up = 3, down = 3):
        self.name = " "
        self.maxReps = maxReps
        self.doneReps = 0
    def playSet(self):
        for rep in range(self.maxReps):
            sound.playSound(self.up+self.down)


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
            sound.playSound(self.up+self.down)
        self.getResult()
        

def pause(length):
    print("\nWell done... Now rest for "+str(length)+" seconds!")
    for j in range(length):
        sys.stdout.write('\r\a{j}'.format(j=length-j))
        sys.stdout.flush()
        time.sleep(1)


### Testscenario
if __name__ == "__main__":
    training = Trainingsplan()
    training.addExcercise()
    training.startTraining()