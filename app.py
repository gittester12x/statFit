"""Web frontend for the fitness training application."""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import excercise
import threading
import time
import json
import sqlite3
import os
import subprocess
import platform

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup
DB_PATH = 'settings.db'

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    key TEXT UNIQUE,
                    value TEXT
                )''')
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    """Get a setting from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else default

def set_setting(key, value):
    """Set a setting in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Global variables to manage training state
current_training = None
training_thread = None
training_status = {"active": False, "current_exercise": "", "current_set": "", "time_remaining": 0, "should_stop": False}
display_sleep_prevention_active = False

@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')

@app.route('/sounds/<path:filename>')
def serve_sound(filename):
    return send_from_directory(os.path.join(app.root_path, 'sounds'), filename)

def is_training_running():
    global training_thread
    return training_thread is not None and training_thread.is_alive()

@app.route('/start_training', methods=['POST'])
def start_training():
    """Start a new training session."""
    global current_training, training_thread, training_status

    if training_status["active"] and is_training_running():
        return jsonify({"error": "Training already in progress"}), 400

    if training_status["active"] and not is_training_running():
        training_status["active"] = False
        training_status["current_exercise"] = ""
        training_status["current_set"] = ""
        training_status["time_remaining"] = 0
        training_status["should_stop"] = False

    # Get training configuration from request
    data = request.get_json()
    exercises = data.get('exercises', [])
    volume = float(data.get('volume', 0.3))

    # Save settings
    set_setting('volume', volume)
    set_setting('exercises', json.dumps(exercises))

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
    global current_training, training_thread, training_status
    training_status["active"] = False
    training_status["should_stop"] = True
    training_status["current_exercise"] = ""
    training_status["current_set"] = ""
    training_status["time_remaining"] = 0
    current_training = None
    training_thread = None
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

@app.route('/get_setting/<key>')
def get_setting_route(key):
    """Get a setting by key."""
    value = get_setting(key)
    return jsonify({"key": key, "value": value})

@app.route('/set_setting', methods=['POST'])
def set_setting_route():
    """Set a setting."""
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key and value is not None:
        set_setting(key, str(value))
        return jsonify({"message": "Setting saved"})
    return jsonify({"error": "Invalid key or value"}), 400

@app.route('/load_settings')
def load_settings():
    """Load saved settings."""
    volume = get_setting('volume', '0.3')
    exercises = get_setting('exercises', '[]')
    try:
        exercises = json.loads(exercises)
    except:
        exercises = []
    return jsonify({"volume": float(volume), "exercises": exercises})

def status_update(status):
    """Update training status from the training thread."""
    global training_status
    if training_status.get("should_stop", False):
        status = dict(status)
        if status.get("active", False):
            status["active"] = False
        status["current_exercise"] = "Stopping..."
        status["current_set"] = ""
    training_status.update(status)

def check_should_stop():
    """Check if training should be stopped."""
    global training_status
    return training_status.get("should_stop", False)

def prevent_display_sleep_thread():
    """Background thread to keep display awake on Windows."""
    from pynput.keyboard import Controller, Key
    import time
    keyboard = Controller()
    while display_sleep_prevention_active:
        time.sleep(30)
        try:
            # Press and release Shift key (neutral key)
            keyboard.press(Key.shift)
            keyboard.release(Key.shift)
        except Exception as e:
            print(f"Error simulating keyboard activity: {e}")

def prevent_display_sleep():
    """Start preventing display sleep based on OS."""
    global display_sleep_prevention_active
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        try:
            process = subprocess.Popen(['caffeinate', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return ('caffeinate', process)
        except Exception as e:
            print(f"Failed to start caffeinate: {e}")
            return None
    
    elif system == 'Windows':
        try:
            display_sleep_prevention_active = True
            thread = threading.Thread(target=prevent_display_sleep_thread, daemon=True)
            thread.start()
            return ('windows', thread)
        except Exception as e:
            print(f"Failed to start keep-alive on Windows: {e}")
            return None
    
    elif system == 'Linux':
        try:
            subprocess.run(['xset', 's', 'off'], check=False, capture_output=True)
            subprocess.run(['xset', 'dpms', 'force', 'on'], check=False, capture_output=True)
            return ('linux', None)
        except Exception as e:
            print(f"Failed to disable display sleep on Linux: {e}")
            return None
    
    return None

def stop_display_sleep_prevention(sleep_preventer):
    """Stop preventing display sleep."""
    global display_sleep_prevention_active
    if not sleep_preventer:
        return
    
    system, process = sleep_preventer
    
    if system == 'caffeinate':
        try:
            process.terminate()
            process.wait(timeout=2)
        except Exception as e:
            print(f"Failed to stop caffeinate: {e}")
    
    elif system == 'windows':
        display_sleep_prevention_active = False
    
    elif system == 'linux':
        try:
            subprocess.run(['xset', 's', 'on'], check=False, capture_output=True)
        except Exception as e:
            print(f"Failed to restore display sleep on Linux: {e}")

def run_training():
    """Run the training session in a separate thread."""
    global current_training, training_status

    # Start preventing display sleep (cross-platform)
    sleep_preventer = prevent_display_sleep()

    try:
        current_training.start_training(pause_duration=60)
        training_status["active"] = False
        training_status["current_exercise"] = "Training Complete!"
        training_status["current_set"] = ""
        training_status["time_remaining"] = 0
    except Exception as e:
        training_status["active"] = False
        training_status["current_exercise"] = f"Error: {str(e)}"
    finally:
        # Stop preventing display sleep when training ends
        stop_display_sleep_prevention(sleep_preventer)

if __name__ == '__main__':
    port = 5000 if os.environ.get('FLASK_ENV') == 'production' else 5001
    app.run(debug=True, host='0.0.0.0', port=port)