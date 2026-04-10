"""Main entry point for the training application."""
import excercise

if __name__ == "__main__":
    training = excercise.Trainingsplan()
    training.add_exercise()
    training.start_training()