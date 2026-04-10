import time
import os
from pynput import keyboard

import soundEffects as sound


def clear_screen():
    """Clear the console screen in a cross-platform way."""
    os.system('cls' if os.name == 'nt' else 'clear')

class Trainingsplan:
    """Main training plan class."""

    def __init__(self):
        self.begin = None
        self.end = None
        self.exercises = []

    def add_exercise(self, name="Exercise", max_reps=10, sets=4, up=3, down=3):
        """Add an exercise to the training plan."""
        exercise = Exercise(name=name)
        for i in range(sets):
            set_name = f"{exercise.name}.{i + 1}"
            exercise.add_set(name=set_name, max_reps=max_reps, up=up, down=down)
        self.exercises.append(exercise)

    def start_training(self, pause_duration=60):
        """Start the training session."""
        clear_screen()
        self.begin = time.time()
        print(f"Training started at {self.begin}")
        for exercise in self.exercises:
            exercise.start_exercise(pause_duration)
        self.end = time.time()

    def print_result(self):
        """Print the training results."""
        clear_screen()
        for exercise in self.exercises:
            print(f"{exercise.name}:")
            print(f"  From {exercise.begin} to {exercise.end}")
            print(f"  Positive phase: {exercise.up}s. Negative phase: {exercise.down}s.")
            print("  Exercise performance: ", end="")
            for set_item in exercise.sets:
                print(f"{set_item.done_reps}/{set_item.max_reps}", end=" ")
            print()




class Exercise:
    """Single exercise in a training plan."""

    def __init__(self, name="Exercise"):
        self.name = name
        self.begin = None
        self.end = None
        self.pause = None
        self.sets = []
        self.up = 0
        self.down = 0

    def add_set(self, name="Exercise", max_reps=10, up=3, down=3):
        """Add a set to this exercise."""
        self.up = up
        self.down = down
        set_item = Set(name=name, max_reps=max_reps, up=up, down=down)
        self.sets.append(set_item)

    def start_exercise(self, pause_duration=60):
        """Start performing this exercise."""
        self.pause = pause_duration
        self.begin = time.time()
        print(f"Starting {self.name}")
        for i, set_item in enumerate(self.sets):
            set_item.play_set()
            rest_period(pause_duration, self.name, i)
        self.end = time.time()

class Set:
    """A single set within an exercise."""

    def __init__(self, name="Exercise", max_reps=10, up=3, down=3):
        self.name = name
        self.max_reps = max_reps
        self.done_reps = 0
        self.up = up
        self.down = down

    def play_set(self):
        """Play through this set of repetitions."""
        rep = 0
        while rep < self.max_reps:
            clear_screen()
            print(self.name)
            print(f"{rep + 1} of {self.max_reps}")
            print("\n\n\n")
            print("Press ENTER to abort set")
            self.done_reps = rep + 1
            sound.play_sound(self.up + self.down)
            rep += 1
            if self.detect_key_press():
                break

    def detect_key_press(self):
        """Detect key press and return True if ENTER is pressed."""
        def on_press(key):
            try:
                if key == keyboard.Key.enter:
                    return False  # Stop listener
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join(timeout=0.1)
        return False


def rest_period(length, exercise, number):
    """Display a rest period between sets."""
    clear_screen()
    print(f"Well done... Now rest for {length} seconds!")
    for j in range(length):
        if j == length - 10:
            sound.play_effect("gong")
        clear_screen()
        time_left = length - j
        print(f"Time until training continues: {time_left}")
        print(f"\n\nCurrent exercise: {exercise}. Set number {number + 1}")
        time.sleep(1)

if __name__ == "__main__":
    training = Trainingsplan()
    rest_period(10, "Start", 0)
    training.add_exercise(name="Pushups", max_reps=8, sets=3, up=3, down=3)
    training.add_exercise(name="Situps", max_reps=8, sets=3, up=3, down=3)
    training.add_exercise(name="Planks", max_reps=8, sets=3, up=3, down=3)
    training.add_exercise(name="Rückenzieher", max_reps=8, sets=3, up=3, down=3)
    training.add_exercise(name="Kniebeugen", max_reps=10, sets=3, up=3, down=3)
    training.start_training(pause_duration=60)
    training.print_result()
    time.sleep(10)