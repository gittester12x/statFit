"""Sound effects module for training application."""
import os
import time

# Allow an explicit dummy audio fallback for containerized environments
if os.environ.get('FORCE_DUMMY_AUDIO', '0') == '1':
    os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

from pygame import mixer

DEFAULT_VOLUME = 0.3


def _init_mixer():
    if not mixer.get_init():
        try:
            mixer.init()
        except Exception as e:
            print(f"Audio initialization failed: {e}")
            if os.environ.get('SDL_AUDIODRIVER') != 'dummy':
                os.environ['SDL_AUDIODRIVER'] = 'dummy'
                try:
                    mixer.quit()
                    mixer.init()
                except Exception as e2:
                    print(f"Audio initialization failed with dummy driver too: {e2}")
            else:
                print("Audio not available; continuing without sound.")


def play_sound(duration, volume=DEFAULT_VOLUME):
    """Play a sound for the specified duration."""
    sound_file = os.path.join(os.getcwd(), 'sounds', '3sec.wav')

    if duration == 6:
        try:
            _init_mixer()
            if mixer.get_init():
                sound = mixer.Sound(sound_file)
                sound.set_volume(volume)
                sound.play()
                time.sleep(6)
        except Exception as e:
            print(f"Playing sound failed: {e}")
            time.sleep(6)  # Still wait the duration


def play_effect(effect="gong", volume=DEFAULT_VOLUME):
    """Play a sound effect."""
    sound_file = os.path.join(os.getcwd(), 'sounds', 'gong.mp3')
    if effect == "gong":
        try:
            _init_mixer()
            if mixer.get_init():
                sound = mixer.Sound(sound_file)
                sound.set_volume(volume)
                sound.play()
        except Exception as e:
            print(f"Playing effect failed: {e}")


if __name__ == "__main__":
    play_sound(6)
