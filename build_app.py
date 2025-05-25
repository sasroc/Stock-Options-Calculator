import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'stock_options_calculator.py',
    '--name=Stock Options Calculator',
    '--windowed',
    '--add-data=venv/lib/python3.13/site-packages/customtkinter:customtkinter',
    '--icon=app_icon.png',
    '--clean',
    '--noconfirm',
]) 