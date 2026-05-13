# StatFit - Cross-Platform Fitness Training Application

A modern, cross-platform fitness training application with web interface, real-time status tracking, and audio cues.

## 🚀 Quick Start

### Option 1: Local Installation (Recommended for Development)

```bash
# Clone and setup
git clone <your-repo-url>
cd statfit

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app (listens on http://localhost:5001)
python3 app.py
```

### Option 2: Docker/Podman Deployment (Recommended for Production)

```bash
# Build and start the container
podman compose -f podman-compose.yaml up --build -d

# App will be available at http://localhost:8080
```

> Note: Audio playback inside a container is not guaranteed on macOS/Podman because the container often has no access to the host sound subsystem. For reliable sound, run the app locally with Python.

## Features

- 🏋️ **Custom Training Plans**: Create personalized workout routines
- 💾 **Settings Persistence**: Automatic save/load of exercises and volume preferences
- 🌐 **Web Interface**: Modern browser-based training experience
- 🔊 **Audio Cues**: Sound effects and timing guidance with error handling
- 📊 **Real-time Status**: Live progress tracking and countdowns
- 🖥️ **Cross-Platform Display Prevention**: Keeps screen awake during training (Windows, macOS, Linux)
- 🐳 **Containerized**: Full Docker/Podman support with automatic deployment
- 📱 **Responsive Design**: Works on desktop and tablet devices

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Option 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd statfit

# Create virtual environment (recommended on macOS and some Linux systems)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Option 2: Manual Installation

If you prefer to install dependencies manually:

```bash
pip install Flask>=2.0.0 pygame>=2.0.0 pynput>=1.7.0
```

### Platform-Specific Setup

#### Linux (Ubuntu/Debian)
```bash
# Install system audio libraries (if needed)
sudo apt-get install libsdl2-dev libsdl2-mixer-dev
```

#### macOS
On macOS, Python packages must be installed in a virtual environment due to system restrictions.

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

No additional system libraries required - works out of the box!

**Network Issues on macOS:**
If you can't access the server on macOS, try these solutions:

1. **Try alternative URLs:**
   - `http://localhost:5000` (or your port number)
   - `http://127.0.0.1:5000`
   - `http://0.0.0.0:5000`

2. **Check firewall settings:**
   - Go to System Settings → Network → Firewall
   - Ensure Python/Flask can accept incoming connections

3. **Try a different browser:**
   - Safari, Chrome, Firefox, or Edge

4. **Check if the server is running:**
   - Look for the "🚀 Starting StatFit..." message in terminal
   - The terminal will show the exact URL to use

#### Windows
No additional setup required - works out of the box!

## 🎯 Usage

### Web Interface (Recommended)

The web interface provides the best user experience with real-time status updates.

1. **Start the web server**:
   ```bash
   python run.py
   ```

2. **Open your browser**:
   - Go to `http://localhost:5000`
   - Your default training plan will be loaded automatically

3. **Start training**:
   - Click "Start Training"
   - Follow the guided workout with live status updates
   - Use "Stop Training" to end the session anytime

### Command Line Interface

For terminal-based training:

```bash
python main.py
```

Or run the exercise module directly:

```bash
python excercise.py
```

## 📁 Project Structure

```
statfit/
├── app.py              # Flask web application
├── excercise.py        # Core training logic and classes
├── soundEffects.py     # Audio handling module
├── main.py            # CLI entry point
├── run.py             # Web server launcher
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/
│   └── index.html     # Web interface template
├── sounds/            # Audio files directory
│   ├── 3sec.wav      # Exercise timing sound
│   └── gong.mp3      # Rest period alert
└── .gitignore        # Git ignore patterns
```

## 🔧 Dependencies

### Core Dependencies

- **Flask** (>=2.0.0): Web framework for the browser interface
- **pygame** (>=2.0.0): Audio playback for sound effects
- **pynput** (>=1.7.0): Cross-platform keyboard input detection

### System Requirements

- **Linux**: SDL2 development libraries (usually pre-installed)
- **macOS**: Works out of the box
- **Windows**: Works out of the box

## 🔊 Sound Files

Place your audio files in the `sounds/` directory:

- `3sec.wav`: Sound played during exercise timing
- `gong.mp3`: Alert sound for rest period transitions

## 🐛 Troubleshooting

### Audio Issues
- Ensure sound files exist in the `sounds/` directory
- Check system audio settings
- On Linux, verify SDL2 libraries are installed

### Keyboard Input Issues
- Ensure your terminal/application has keyboard focus
- On some systems, you may need to run with elevated privileges

### Web Interface Issues
- Ensure port 5000 is not blocked by firewall
- Try a different browser if issues persist
- Check that the server is actually running (look for startup messages in terminal)

**Can't find/access the server?**
- **Check the terminal output** - it shows the exact URL to use
- **Try alternative URLs:**
  - `http://localhost:[port]`
  - `http://127.0.0.1:[port]`
  - `http://0.0.0.0:[port]`
- **Firewall issues:** Ensure your firewall allows Python/Flask connections
- **Port conflicts:** The app automatically finds available ports, but check if another service is blocking access
- **Network restrictions:** Some corporate networks block local servers

### Safari on macOS Issues

If Safari won't load the page, try these solutions:

1. **Allow insecure localhost connections:**
   - In Safari, go to **Safari → Settings → Privacy**
   - Uncheck "Prevent cross-site tracking" temporarily
   - Or try **Develop → Disable Local File Restrictions** (if Develop menu is enabled)

2. **Enable Develop menu:**
   - Go to **Safari → Settings → Advanced**
   - Check "Show Develop menu in menu bar"
   - Then try **Develop → Disable Local File Restrictions**

3. **Try a different browser:**
   - Chrome: `http://localhost:[port]`
   - Firefox: `http://localhost:[port]`
   - Or use `http://127.0.0.1:[port]` in any browser

4. **Check macOS firewall:**
   - Go to **System Settings → Network → Firewall**
   - Ensure it's not blocking Python or Flask

5. **Try with 0.0.0.0 binding:**
   - The app now tries `0.0.0.0` first on macOS
   - Try: `http://0.0.0.0:[port]` in your browser

### Common Installation Issues

**"Module not found" errors:**
```bash
# Make sure you're in the project directory
cd statfit

# Install dependencies
pip install -r requirements.txt
```

**Permission errors on Linux/macOS:**
```bash
# Run with your user account (don't use sudo for pip)
pip install -r requirements.txt
```

**Port 5000 already in use:**
StatFit automatically finds an available port starting from 5000. Check the terminal output for the exact URL to use.

## 🛠️ Development

### Running Tests

```bash
# Test CLI version
python main.py

# Test web interface
python run.py
```

### Code Style

The project follows PEP 8 Python style guidelines with:
- Snake_case naming for functions and variables
- Docstrings for all classes and methods
- Cross-platform compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 💬 Support

For issues and questions:
- Check the troubleshooting section above
- Ensure all dependencies are properly installed
- Test on multiple platforms if possible

---

**Happy training! 💪**