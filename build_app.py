import PyInstaller.__main__
import os
import sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the icon path is absolute
icon_path = os.path.join(current_dir, "app_icon.ico")

PyInstaller.__main__.run([
    'stock_options_calculator.py',
    '--name=Stock Options Calculator',
    '--windowed',
    f'--icon={icon_path}',  # Use absolute path for icon
    '--clean',
    '--noconfirm',
    '--onefile',
    f'--add-data={icon_path};.',  # Add icon to the bundle
]) 