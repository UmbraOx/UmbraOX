"""
Creates desktop shortcuts for Umbra on Windows.
Run: python create_shortcuts.py
"""
import os
import sys

_UMBRA_ROOT = os.path.dirname(os.path.abspath(__file__))
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
PYTHON = sys.executable


def create_shortcut(name, script, description):
    try:
        import winreg
        shortcut_path = os.path.join(DESKTOP, f"{name}.bat")
        bat_content = f"""@echo off
title {name}
cd /d "{_UMBRA_ROOT}"
call venv\\Scripts\\activate.bat
{PYTHON} {os.path.join(_UMBRA_ROOT, script)} %*
"""
        with open(shortcut_path, "w") as f:
            f.write(bat_content)
        print(f"  Created: {shortcut_path}")
        return shortcut_path
    except Exception as e:
        print(f"  Error creating {name}: {e}")
        return None


def create_vbs_shortcut(name, bat_path):
    """Create a proper .vbs shortcut that doesn't flash a terminal."""
    try:
        import subprocess
        vbs_path = os.path.join(DESKTOP, f"{name}.vbs")
        # Create shortcut using PowerShell
        ps_cmd = f"""
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{os.path.join(DESKTOP, name + '.lnk')}")
$Shortcut.TargetPath = "{bat_path}"
$Shortcut.WorkingDirectory = "{_UMBRA_ROOT}"
$Shortcut.Description = "UMBRA Autonomous AI Runtime OS"
$Shortcut.Save()
"""
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
        print(f"  Created shortcut: {name}.lnk")
    except Exception as e:
        print(f"  Could not create .lnk: {e}")


if __name__ == "__main__":
    print("\nCreating Umbra desktop shortcuts...")
    print(f"Desktop: {DESKTOP}\n")

    bat1 = create_shortcut("UMBRA Desktop", "umbra_desktop.py", "Umbra Desktop App")
    bat2 = create_shortcut("UMBRA GUI (Browser)", "gui_server.py", "Umbra Browser GUI")
    bat3 = create_shortcut("UMBRA CLI", "umbra.py", "Umbra Command Line")

    for name, bat in [("UMBRA Desktop", bat1), ("UMBRA GUI", bat2), ("UMBRA CLI", bat3)]:
        if bat:
            create_vbs_shortcut(name, bat)

    print(f"\nDone! Check your Desktop for shortcuts.")
    print("Double-click 'UMBRA Desktop' to launch the desktop app.")
    print("Double-click 'UMBRA GUI (Browser)' to launch the web interface.")