from pygame import mixer  # Load the popular external library
import time

def playSound(duration):
    if duration == 6:
        mixer.init()
        sound = mixer.Sound('/home/paul/Programming/statFit/sounds/3sec.wav')
        sound.play()
        time.sleep(6)

