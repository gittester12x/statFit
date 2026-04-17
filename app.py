"""Web frontend for the fitness training application."""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import excercise
import threading
import time
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to manage training state
current_training = None
training_thread = None
training_status = {"active": False, "current_exercise": "", "current_set": "", "time_remaining": 0, "should_stop": False}

@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')

@app.route('/start_training', methods=['POST'])
def start_training():
    """Start a new training session."""
    global current_training, training_thread, training_status

    if training_status["active"]:
        return jsonify({"error": "Training already in progress"}), 400

    # Get training configuration from request
    data = request.get_json()
    exercises = data.get('exercises', [])
    volume = float(data.get('volume', 0.3))

    # Create training plan
    current_training = excercise.Trainingsplan(status_callback=status_update, stop_check_callback=check_should_stop, volume=volume)

    # Add exercises
    for ex in exercises:
        current_training.add_exercise(
            name=ex['name'],
            max_reps=ex['max_reps'],
            sets=ex['sets'],
            up=ex['up'],
            down=ex['down']
        )

    # Start training in background thread
    training_status["active"] = True
    training_status["should_stop"] = False
    training_thread = threading.Thread(target=run_training)
    training_thread.daemon = True
    training_thread.start()

    return jsonify({"message": "Training started"})

@app.route('/stop_training', methods=['POST'])
def stop_training():
    """Stop the current training session."""
    global training_status
    training_status["active"] = False
    training_status["should_stop"] = True
    return jsonify({"message": "Training stopped"})

@app.route('/get_status')
def get_status():
    """Get current training status."""
    return jsonify(training_status)

@app.route('/get_results')
def get_results():
    """Get training results."""
    if current_training:
        return jsonify({"results": current_training.get_results()})
    return jsonify({"results": []})

def status_update(status):
    """Update training status from the training thread."""
    global training_status
    training_status.update(status)

def check_should_stop():
    """Check if training should be stopped."""
    global training_status
    return training_status.get("should_stop", False)

def run_training():
    """Run the training session in a separate thread."""
    global current_training, training_status

    try:
        current_training.start_training(pause_duration=60)
        training_status["active"] = False
        training_status["current_exercise"] = "Training Complete!"
        training_status["current_set"] = ""
        training_status["time_remaining"] = 0
    except Exception as e:
        training_status["active"] = False
        training_status["current_exercise"] = f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)