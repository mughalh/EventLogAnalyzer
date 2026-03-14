# Windows Event Log Analyzer

A modern, powerful GUI tool to analyze Windows Event Log files (.evtx) and troubleshoot system crashes, unexpected shutdowns, and errors.



## 🚀 Quick Start

1. **Download** the latest `EventLogAnalyzer.exe` from [Releases](https://github.com/yourusername/windows-event-log-analyzer/releases)
2. **Run** the executable (no installation needed)
3. **Drag & drop** your `.evtx` files or use File → Open
4. **Click** any quick analysis button to find issues

---

## ✨ Features

### 📂 File Operations
- **Drag & drop** support for .evtx files
- Open multiple files or entire folders
- View loaded files in a handy list
- Remove files with double-click

### ⚡ One-Click Analysis
| Button | What it Finds |
|--------|--------------|
| 💥 Crashes | BugCheck events (BSOD) - Event ID 1001 |
| 🔌 Shutdowns | Unexpected shutdowns - Event ID 41 |
| ❌ Critical | All Critical level events |
| ⚠️ Errors | All Error and Critical events |
| 💾 Disk | Disk, volume, and filesystem errors |
| 📊 Last 50 | Most recent 50 events |

### 🔍 Advanced Filtering
- Filter by **Event ID**
- Filter by **Level** (Critical/Error/Warning/Information)
- Filter by **Provider** (source of the event)
- Full-text **search** within event data
- **Bookmark** important events for later

### 📊 Multi-Tab Details
| Tab | Description |
|-----|-------------|
| **Summary** | Formatted event overview with key information |
| **Raw XML** | Complete XML data for advanced analysis |
| **Data Fields** | Tree view of all event data fields |
| **Bookmarks** | Collection of your saved events |

### 📈 Statistics Dashboard
Real-time counts showing:
- Total events loaded
- Critical events
- Errors
- Warnings
- Information events
- Bookmarked events

### 💾 Export Options
- **CSV** format for spreadsheet analysis
- **JSON** format for structured data
- **Text** format for readable reports
- **Single event** export
- **Summary reports** with statistics

### ⌨️ Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open files |
| `Ctrl+E` | Export results |
| `Ctrl+F` | Search events |
| `Ctrl+B` | Bookmark current event |
| `Ctrl+D` | Toggle dark mode |

### 🎨 Modern UI
- Clean, professional interface
- Color-coded events (red=critical, yellow=error)
- Hover effects and visual feedback
- Dark mode support
- Resizable windows with proper scaling

---

## 📥 Download

| Version | Architecture | Link |
|---------|--------------|------|
| v1.0 | 64-bit (x64) | [Download EventLogAnalyzer.exe](https://github.com/yourusername/windows-event-log-analyzer/releases/latest) |

**Note for ARM64 users:** Windows ARM64 can run x64 apps through emulation. Native ARM64 version coming soon.

---

## 🖱️ How to Use

### Basic Usage
1. **Launch the application**
2. **Open your event logs** - Drag & drop .evtx files or use File → Open
3. **Quick analyze** - Click any quick analysis button
4. **Explore** - Click events to see details
5. **Bookmark** - Save important events (Ctrl+B)
6. **Export** - Save your findings

### Finding Crash Causes
```
1. Open System.evtx from the crashed Windows machine
2. Click "Crashes" to find all BSOD events
3. Review the stop code and parameters
4. Check surrounding events for clues
5. Export the findings for reference
```

### Investigating Shutdowns
```
1. Load the System.evtx file
2. Click "Shutdowns" to find Event ID 41 entries
3. Look at events before the shutdown
4. Check for disk errors or driver failures
5. Bookmark relevant events
```

---

## 📋 Requirements

### For Users (Running the .exe)
- Windows 7 or later (Windows 10/11 recommended)
- 50 MB free disk space
- No Python installation needed

### For Developers (Building from source)
- Python 3.6 or higher
- python-evtx library
- PyInstaller (for creating executable)

---

## 🔧 Building from Source

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/windows-event-log-analyzer.git
cd windows-event-log-analyzer
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python event_log_analyzer_modern.py
```

### 5. Build executable
```bash
# Simple build
pyinstaller --onefile --windowed --name "EventLogAnalyzer" event_log_analyzer_modern.py

# Build with optimizations
pyinstaller --onefile --windowed --name "EventLogAnalyzer" --clean --noconfirm --hidden-import=evtx event_log_analyzer_modern.py
```

The executable will be in the `dist` folder.

---

## 📁 Project Structure

```
windows-event-log-analyzer/
├── event_log_analyzer_modern.py   # Main application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── LICENSE                          # MIT License
└── .github/
    └── workflows/                    # GitHub Actions
        └── build.yml                  # Auto-build on releases
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- [python-evtx](https://github.com/williballenthin/python-evtx) for EVTX parsing
- [PyInstaller](https://pyinstaller.org/) for creating standalone executables
- All contributors and users

---

## 📧 Contact

Project Link: [https://github.com/yourusername/windows-event-log-analyzer](https://github.com/yourusername/windows-event-log-analyzer)

Report issues: [GitHub Issues](https://github.com/yourusername/windows-event-log-analyzer/issues)

---

**Made for Windows administrators, support technicians, and anyone trying to figure out why their PC keeps crashing.**

<p align="center">
  <a href="#windows-event-log-analyzer">Back to Top ↑</a>
</p>
