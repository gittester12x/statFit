import pandas as pd
import datetime 
import time
import soundEffects as sound
import sys
import os
import keyboard  # using module keyboard
import select 
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
            excercise.addSet(name=excercise.name+"."+excercise.name,maxReps=10,up=up,down=down)
        self.excercises.append(excercise)

    def startTraining(self,pauseDuration = 60,warmup = True):
        os.system('clear')
        beginn = pd.Timestamp(datetime.datetime.now())
        print("Training started at "+str(beginn))
        for excercise in self.excercises:
            excercise.startExcercise(pauseDuration)
        end = pd.Timestamp(datetime.datetime.now())

    def printResult(self):
        os.system('clear')
        for excercise in self.excercises:
            print(excercise.name+": ",end="")
            for set in excercise.sets:
                print(str(set.doneReps)+"/"+str(set.maxReps),end=" ")
            print()

class Excercise:
    def __init__(self,name = "Excercise"):
        self.name = name
        self.beginn = None
        self.end = None
        self.pause = None
        self.sets = []

    def addSet(self,name = "Excercise",maxReps = 10, up = 3, down = 3):
        set = Set(name = name,maxReps = 10, up = 3, down = 3)
        self.sets.append(set)
        

    def startExcercise(self,pauseDuration = 60):
        print("Starting  "+self.name)
        for i in range(len(self.sets)):
            self.sets[i].playSet()
            pause(pauseDuration)
            
            
class Set:
    def __init__(self,name = "Excercise",maxReps = 10, up = 3, down = 3):
        print("Set added with name"+name)
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
                self.doneReps=rep
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
    training.addExcercise(name = "Pushups", maxReps = 10, sets = 2, up = 3, down = 3)
    training.addExcercise(name = "Situps", maxReps = 10, sets = 2, up = 3, down = 3)
    #training.addExcercise(name = "Planks", maxReps = 10, sets = 2, up = 3, down = 3)
    #training.addExcercise(name = "Rückenzieher", maxReps = 10, sets = 4, up = 3, down = 3)
    #training.addExcercise(name = "Kniebeugen links", maxReps = 10, sets = 3, up = 3, down = 3)
    #training.addExcercise(name = "Kniebeugen rechts", maxReps = 10, sets = 3, up = 3, down = 3)
    training.startTraining(pauseDuration=1)
    training.printResult()
    time.sleep(10)

