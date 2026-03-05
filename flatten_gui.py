#!/usr/bin/env python3
import json
import sys
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
    root.title("OrcaSlicer Filament Flattener")
    root.geometry("500x300")

    label = tk.Label(
        root,
        text="Drop filament JSON here",
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
            text="Drag‑and‑drop requires tkinterdnd2.\n\nInstall:\npip install tkinterdnd2"
        )

    root.mainloop()


if __name__ == "__main__":
    main()

