import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image, ImageTk

def test_icon():
    # Test with regular tkinter first
    print("Testing with regular tkinter...")
    root_tk = tk.Tk()
    root_tk.title("Tkinter Test")
    icon_path = os.path.abspath("app_icon.ico")
    print(f"Icon path: {icon_path}")
    print(f"File exists: {os.path.exists(icon_path)}")
    
    if os.path.exists(icon_path):
        try:
            root_tk.iconbitmap(icon_path)
            print("Icon set successfully in tkinter window")
        except Exception as e:
            print(f"Tkinter icon error: {e}")
    
    # Test with customtkinter
    print("\nTesting with customtkinter...")
    root_ctk = ctk.CTk()
    root_ctk.title("CustomTkinter Test")
    
    if os.path.exists(icon_path):
        try:
            # Try multiple methods
            print("Method 1: Direct iconbitmap")
            root_ctk.iconbitmap(icon_path)
        except Exception as e:
            print(f"Method 1 error: {e}")
            try:
                print("Method 2: Using _w")
                root_ctk._w.iconbitmap(icon_path)
            except Exception as e:
                print(f"Method 2 error: {e}")
                try:
                    print("Method 3: Using PhotoImage")
                    icon_image = Image.open(icon_path)
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    root_ctk.iconphoto(True, icon_photo)
                except Exception as e:
                    print(f"Method 3 error: {e}")
    
    # Keep both windows open
    root_tk.mainloop()
    root_ctk.mainloop()

if __name__ == "__main__":
    test_icon()