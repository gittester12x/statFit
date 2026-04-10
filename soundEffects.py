"""Sound effects module for training application."""
import time
import os
from pygame import mixer


def play_sound(duration):
    """Play a sound for the specified duration."""
    sound_file = os.path.join(os.getcwd(), 'sounds', '3sec.wav')

    if duration == 6:
        mixer.init()
        sound = mixer.Sound(sound_file)
        sound.play()
        time.sleep(6)


def play_effect(effect="gong"):
    """Play a sound effect."""
    sound_file = os.path.join(os.getcwd(), 'sounds', 'gong.mp3')
    if effect == "gong":
        mixer.init()
        sound = mixer.Sound(sound_file)
        sound.play()


if __name__ == "__main__":
    play_sound(6)
