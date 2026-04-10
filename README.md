# StatFit - Cross-Platform Fitness Training Application

A modern, cross-platform fitness training application with both web and command-line interfaces.

## 🚀 Quick Start

**Want to get started immediately?**

```bash
# 1. Download/clone the project
git clone <your-repo-url>
cd statfit

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the web app
python run.py

# 4. Open http://localhost:5000 in your browser
```

**Note**: If port 5000 is already in use, StatFit will automatically use the next available port (5001, 5002, etc.). Check the terminal output for the exact URL.

That's it! Your training plan loads automatically. Click "Start Training" and begin! 💪

## Features

- 🏋️ **Custom Training Plans**: Create personalized workout routines
- 🌐 **Web Interface**: Modern browser-based training experience
- ⌨️ **CLI Mode**: Command-line interface for terminal users
- 🔊 **Audio Cues**: Sound effects and timing guidance
- 📊 **Real-time Status**: Live progress tracking and countdowns
- 🖥️ **Cross-Platform**: Works on Linux, macOS, and Windows
- 🎯 **Keyboard Control**: Interactive training with keyboard input

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Option 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd statfit

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
No additional setup required - works out of the box!

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