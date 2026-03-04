OrcaSlicer Preset Flattener (GUI)
A drag‑and‑drop GUI tool for flattening OrcaSlicer preset JSON files.
Supports filament, process, and printer presets by resolving inheritance chains and producing fully explicit, standalone JSON files.

This tool is designed for users who want complete control over their OrcaSlicer profiles, including those building material‑aware or printer‑agnostic preset libraries.

✨ Features
Drag‑and‑drop GUI (Tkinter + tkinterdnd2)

Flattens filament, process, and printer presets

Resolves multi‑level inheritance (inherits, parent_id)

Produces explicit _flat.json files with no hidden defaults

Works on Linux with Python 3.13+

Optional desktop launcher for one‑click access

📦 Requirements
Python 3.13 or newer

Tkinter (system package)

tkinterdnd2 (installed inside a virtual environment)

🛠️ Installation
1. Create a virtual environment
bash
python3 -m venv flatten-env
Activate it:

bash
source flatten-env/bin/activate
2. Install Tkinter (system package)
For Python 3.13:

bash
sudo apt install python3.13-tk
3. Install tkinterdnd2 (inside the venv)
bash
pip install tkinterdnd2
🪟 GUI Script
Save this as flatten_gui.py in your home directory:

python
#!/usr/bin/env python3
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

try:
    import tkinterdnd2 as tkdnd
    DND = True
except ImportError:
    DND = False


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_inheritance(profile: dict, base_dir: Path):
    merged = {}

    while True:
        parent = profile.get("parent_id") or profile.get("inherits")
        if not parent:
            break

        parent_path = base_dir / f"{parent}.json"
        if not parent_path.exists():
            raise FileNotFoundError(f"Parent preset not found:\n{parent_path}")

        parent_json = load_json(parent_path)
        merged.update(parent_json)
        profile = {**parent_json, **profile}

    merged.update(profile)
    merged.pop("parent_id", None)
    merged.pop("inherits", None)
    return merged


def flatten_file(path_str):
    input_path = Path(path_str.strip().strip("{}"))
    if not input_path.exists():
        messagebox.showerror("Error", f"File not found:\n{input_path}")
        return

    try:
        profile = load_json(input_path)
        base_dir = input_path.parent
        flattened = resolve_inheritance(profile, base_dir)

        output_path = input_path.with_name(input_path.stem + "_flat.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(flattened, f, indent=2)

        messagebox.showinfo("Success", f"Flattened file saved:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def main():
    root = tkdnd.Tk() if DND else tk.Tk()
    root.title("OrcaSlicer Preset Flattener")
    root.geometry("500x300")

    label = tk.Label(
        root,
        text="Drop preset JSON here",
        relief="groove",
        borderwidth=3,
        font=("Arial", 16),
        bg="#f0f0f0"
    )
    label.pack(expand=True, fill="both", padx=20, pady=20)

    if DND:
        label.drop_target_register("DND_Files")
        label.dnd_bind("<<Drop>>", lambda e: flatten_file(e.data))
    else:
        label.config(
            text="Drag‑and‑drop requires tkinterdnd2.\nInstall inside venv:\npip install tkinterdnd2"
        )

    root.mainloop()


if __name__ == "__main__":
    main()
Make it executable:

bash
chmod +x flatten_gui.py
▶️ Running the GUI
From inside the virtual environment:

bash
./flatten_gui.py
A window will appear.
Drop any OrcaSlicer preset JSON file into it.

The tool writes:

Code
<name>_flat.json
next to the original file.

🖥️ Optional: Desktop Launcher
1. Create the wrapper script
Create:

Code
~/flatten-env/run_flattener.sh
Add:

bash
#!/bin/bash
source "$HOME/flatten-env/bin/activate"
python3 "$HOME/flatten_gui.py"
Make it executable:

bash
chmod +x ~/flatten-env/run_flattener.sh
2. Create the desktop entry
Create:

Code
~/.local/share/applications/filament-flattener.desktop
Add:

ini
[Desktop Entry]
Type=Application
Name=Orca Preset Flattener
Comment=Drag-and-drop GUI to flatten OrcaSlicer presets
Exec=/home/richard/flatten-env/run_flattener.sh
Icon=utilities-terminal
Terminal=false
Categories=Utility;
Make it executable:

bash
chmod +x ~/.local/share/applications/filament-flattener.desktop
Refresh:

bash
update-desktop-database ~/.local/share/applications
You will now see Orca Preset Flattener in your application menu.

📁 Supported Preset Types
The tool supports all OrcaSlicer preset categories:

Filament presets

Process presets

Printer presets

It resolves inheritance chains across:

inherits

parent_id

multi‑level vendor/system defaults

Parent presets must be present in the same exported preset bundle.
