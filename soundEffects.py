"""Sound effects module for training application."""
import time
import os
from pygame import mixer

DEFAULT_VOLUME = 0.3


def _init_mixer():
    if not mixer.get_init():
        mixer.init()


def play_sound(duration, volume=DEFAULT_VOLUME):
    """Play a sound for the specified duration."""
    sound_file = os.path.join(os.getcwd(), 'sounds', '3sec.wav')

    if duration == 6:
        _init_mixer()
        sound = mixer.Sound(sound_file)
        sound.set_volume(volume)
        sound.play()
        time.sleep(6)


def play_effect(effect="gong", volume=DEFAULT_VOLUME):
    """Play a sound effect."""
    sound_file = os.path.join(os.getcwd(), 'sounds', 'gong.mp3')
    if effect == "gong":
        _init_mixer()
        sound = mixer.Sound(sound_file)
        sound.set_volume(volume)
        sound.play()


if __name__ == "__main__":
    play_sound(6)
