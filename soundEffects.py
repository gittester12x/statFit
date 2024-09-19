from pygame import mixer  # Load the popular external library
import time
import os

def playSound(duration):
    cwd = os.getcwd() 
    file = cwd+'/sounds/3sec.wav'
    
    if duration == 6:
        mixer.init()
        sound = mixer.Sound(file)
        sound.play()
        time.sleep(6)

def playEffect(effect="gong"):
    cwd = os.getcwd() 
    file = cwd+'/sounds/gong.mp3'
    if effect=="gong":
        mixer.init()
        sound = mixer.Sound(file)
        sound.play()
        

if __name__ == "__main__":
    playSound(6)
    import sys
    print(sys.version)
