# OrcaSlicer Preset Flattener (GUI)
A drag‑and‑drop GUI tool for flattening OrcaSlicer preset JSON files.
Supports filament, process, and printer presets by resolving inheritance chains and producing fully explicit, standalone JSON files.

This tool is designed for users who want complete control over their OrcaSlicer profiles, including those building material‑aware or printer‑agnostic preset libraries.
# ✨ Features
- Drag‑and‑drop GUI (Tkinter + tkinterdnd2)

- Flattens filament, process, and printer presets

- Resolves multi‑level inheritance (inherits, parent_id)

- Produces explicit _flat.json files with no hidden defaults

- Works on Linux with Python 3.13+

- Optional desktop launcher for one‑click access
# 📦 Requirements
- Python 3.13 or newer

- Tkinter (system package)

- tkinterdnd2 (installed inside a virtual environment)
## 🛠️ Installation
### 1. Create a virtual environment
`python3 -m venv flatten-env`
