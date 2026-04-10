import time
import os
from pynput import keyboard

import soundEffects as sound


def clear_screen():
    """Clear the console screen in a cross-platform way."""
    os.system('cls' if os.name == 'nt' else 'clear')

class Trainingsplan:
    """Main training plan class with web frontend support."""

    def __init__(self, status_callback=None, stop_check_callback=None):
        self.begin = None
        self.end = None
        self.exercises = []
        self.status_callback = status_callback
        self.stop_check_callback = stop_check_callback
        self.current_exercise_index = 0
        self.current_set_index = 0

    def add_exercise(self, name="Exercise", max_reps=10, sets=4, up=3, down=3):
        """Add an exercise to the training plan."""
        exercise = Exercise(name=name, status_callback=self.status_callback, stop_check_callback=self.stop_check_callback)
        for i in range(sets):
            set_name = f"{exercise.name}.{i + 1}"
            exercise.add_set(name=set_name, max_reps=max_reps, up=up, down=down)
        self.exercises.append(exercise)

    def start_training(self, pause_duration=60):
        """Start the training session."""
        clear_screen()
        self.begin = time.time()
        if self.status_callback:
            self.status_callback({"active": True, "current_exercise": "Starting training...", "current_set": "", "time_remaining": 0})

        print(f"Training started at {self.begin}")
        for i, exercise in enumerate(self.exercises):
            # Check if we should stop
            if self.stop_check_callback and self.stop_check_callback():
                break
            self.current_exercise_index = i
            exercise.start_exercise(pause_duration)
        self.end = time.time()

        if self.status_callback:
            self.status_callback({"active": False, "current_exercise": "Training Complete!", "current_set": "", "time_remaining": 0})

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

    def get_results(self):
        """Get training results as a dictionary."""
        results = []
        for exercise in self.exercises:
            results.append({
                "name": exercise.name,
                "start_time": exercise.begin,
                "end_time": exercise.end,
                "up_time": exercise.up,
                "down_time": exercise.down,
                "sets": [{"done": s.done_reps, "planned": s.max_reps} for s in exercise.sets]
            })
        return results




class Exercise:
    """Single exercise in a training plan."""

    def __init__(self, name="Exercise", status_callback=None, stop_check_callback=None):
        self.name = name
        self.begin = None
        self.end = None
        self.pause = None
        self.sets = []
        self.up = 0
        self.down = 0
        self.status_callback = status_callback
        self.stop_check_callback = stop_check_callback

    def add_set(self, name="Exercise", max_reps=10, up=3, down=3):
        """Add a set to this exercise."""
        self.up = up
        self.down = down
        set_item = Set(name=name, max_reps=max_reps, up=up, down=down, status_callback=self.status_callback, stop_check_callback=self.stop_check_callback)
        self.sets.append(set_item)

    def start_exercise(self, pause_duration=60):
        """Start performing this exercise."""
        self.pause = pause_duration
        self.begin = time.time()
        if self.status_callback:
            self.status_callback({"active": True, "current_exercise": self.name, "current_set": "", "time_remaining": 0})

        print(f"Starting {self.name}")
        for i, set_item in enumerate(self.sets):
            # Check if we should stop
            if self.stop_check_callback and self.stop_check_callback():
                break
            # Update status to show current set
            if self.status_callback:
                self.status_callback({"active": True, "current_exercise": self.name, "current_set": set_item.name, "time_remaining": 0})
            set_item.play_set()
            rest_period(pause_duration, self.name, i, self.status_callback, self.stop_check_callback)
        self.end = time.time()

class Set:
    """A single set within an exercise."""

    def __init__(self, name="Exercise", max_reps=10, up=3, down=3, status_callback=None, stop_check_callback=None):
        self.name = name
        self.max_reps = max_reps
        self.done_reps = 0
        self.up = up
        self.down = down
        self.status_callback = status_callback
        self.stop_check_callback = stop_check_callback

    def play_set(self):
        """Play through this set of repetitions."""
        if self.status_callback:
            self.status_callback({"active": True, "current_exercise": self.name.split('.')[0], "current_set": self.name, "time_remaining": 0})

        rep = 0
        while rep < self.max_reps:
            # Check if we should stop
            if self.stop_check_callback and self.stop_check_callback():
                break
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


def rest_period(length, exercise, number, status_callback=None, stop_check_callback=None):
    """Display a rest period between sets."""
    clear_screen()
    print(f"Well done... Now rest for {length} seconds!")
    for j in range(length):
        # Check if we should stop
        if stop_check_callback and stop_check_callback():
            break
        if j == length - 10:
            sound.play_effect("gong")
        clear_screen()
        time_left = length - j
        if status_callback:
            status_callback({"active": True, "current_exercise": f"Rest after {exercise}", "current_set": "", "time_remaining": time_left})
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