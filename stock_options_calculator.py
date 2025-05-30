import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
import sys
import json
from PIL import Image, ImageTk

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class StockOptionsCalculator:
    def __init__(self):
        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Stock Options Calculator")
        self.root.geometry("800x500")  # Fixed window size
        self.root.minsize(800, 500)    # Set minimum size to prevent shrinking
        
        # Set window icon
        try:
            icon_path = resource_path("app_icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Window icon error: {e}")
        
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)  # Add column for customization
        
        # Title and Customize button frame
        self.title_frame = ctk.CTkFrame(self.main_frame)
        self.title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        self.title_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Stock Options Calculator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 0))
        
        # Customize button
        self.customize_button = ctk.CTkButton(
            self.title_frame,
            text="Customize %'s",
            command=self.toggle_customization,
            width=120
        )
        self.customize_button.grid(row=0, column=1, padx=(10, 0))
        
        # Left side frame (Calculator)
        self.calculator_frame = ctk.CTkFrame(self.main_frame)
        self.calculator_frame.grid(row=1, column=0, padx=(0, 10), sticky="nsew")
        self.calculator_frame.grid_columnconfigure(0, weight=1)
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.calculator_frame)
        self.input_frame.grid(row=0, column=0, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        # Fill price label and entry
        self.fill_price_label = ctk.CTkLabel(
            self.input_frame,
            text="Contract Fill Price:",
            font=ctk.CTkFont(size=14)
        )
        self.fill_price_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.fill_price_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter price (e.g., 2.00)",
            font=ctk.CTkFont(size=14)
        )
        self.fill_price_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Button frame for Calculate and Clear buttons
        self.button_frame = ctk.CTkFrame(self.calculator_frame)
        self.button_frame.grid(row=1, column=0, pady=20)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        
        # Calculate button
        self.calculate_button = ctk.CTkButton(
            self.button_frame,
            text="Calculate",
            command=self.calculate_prices,
            font=ctk.CTkFont(size=14)
        )
        self.calculate_button.grid(row=0, column=0, padx=5)
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self.clear_all,
            font=ctk.CTkFont(size=14),
            fg_color="#FF4444",
            hover_color="#CC0000"
        )
        self.clear_button.grid(row=0, column=1, padx=5)
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.calculator_frame)
        self.results_frame.grid(row=2, column=0, pady=10, sticky="ew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize percentage lists from saved values or defaults
        self.load_percentages()
        
        # Initialize result labels
        self.result_labels = []
        
        # Create customization frame (initially hidden)
        self.customization_frame = ctk.CTkFrame(self.main_frame)
        self.customization_frame.grid(row=1, column=1, padx=(10, 0), sticky="nsew")
        self.customization_frame.grid_remove()  # Hide initially
        
        # Negative percentages section
        self.neg_frame = ctk.CTkFrame(self.customization_frame)
        self.neg_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        ctk.CTkLabel(
            self.neg_frame,
            text="Negative Percentages",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))
        
        self.neg_list_frame = ctk.CTkFrame(self.neg_frame)
        self.neg_list_frame.pack(fill="x", padx=10, pady=5)
        
        self.neg_entry = ctk.CTkEntry(
            self.neg_frame,
            placeholder_text="e.g., -15",
            width=200
        )
        self.neg_entry.pack(pady=5)
        
        ctk.CTkButton(
            self.neg_frame,
            text="Add Negative %",
            command=self.add_negative_percentage
        ).pack(pady=5)
        
        # Positive percentages section
        self.pos_frame = ctk.CTkFrame(self.customization_frame)
        self.pos_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        ctk.CTkLabel(
            self.pos_frame,
            text="Positive Percentages",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))
        
        self.pos_list_frame = ctk.CTkFrame(self.pos_frame)
        self.pos_list_frame.pack(fill="x", padx=10, pady=5)
        
        self.pos_entry = ctk.CTkEntry(
            self.pos_frame,
            placeholder_text="e.g., 15",
            width=200
        )
        self.pos_entry.pack(pady=5)
        
        ctk.CTkButton(
            self.pos_frame,
            text="Add Positive %",
            command=self.add_positive_percentage
        ).pack(pady=5)
        
        # Add Defaults button
        ctk.CTkButton(
            self.customization_frame,
            text="Restore Defaults (-10% & +10%)",
            command=self.restore_defaults,
            fg_color="#1f538d",
            hover_color="#153a63"
        ).pack(pady=10)
        
        # Initialize the percentage lists
        self.update_percentage_lists()
        
        # Bind Enter key to calculate
        self.fill_price_entry.bind('<Return>', lambda event: self.calculate_prices())
        
        # Bind window close event to save percentages
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_percentages(self):
        """Load saved percentages from file or use defaults"""
        try:
            with open('percentages.json', 'r') as f:
                data = json.load(f)
                self.negative_percentages = data.get('negative', [-10])
                self.positive_percentages = data.get('positive', [10])
        except (FileNotFoundError, json.JSONDecodeError):
            # Use defaults if file doesn't exist or is invalid
            self.negative_percentages = [-10]
            self.positive_percentages = [10]
    
    def save_percentages(self):
        """Save current percentages to file"""
        data = {
            'negative': self.negative_percentages,
            'positive': self.positive_percentages
        }
        with open('percentages.json', 'w') as f:
            json.dump(data, f)
    
    def on_closing(self):
        """Handle window closing"""
        self.save_percentages()
        self.root.destroy()
    
    def toggle_customization(self):
        """Toggle the visibility of the customization frame"""
        if self.customization_frame.winfo_viewable():
            self.customization_frame.grid_remove()
            self.customize_button.configure(text="Customize %'s")
        else:
            self.customization_frame.grid()
            self.customize_button.configure(text="Hide Customization")
            self.update_percentage_lists()
    
    def add_negative_percentage(self):
        try:
            value = float(self.neg_entry.get())
            if value >= 0:
                messagebox.showerror("Invalid Input", "Please enter a negative value")
                return
            if value not in self.negative_percentages:
                self.negative_percentages.append(value)
                self.negative_percentages.sort(reverse=True)
                self.update_percentage_lists()
                self.calculate_prices()
                self.save_percentages()
            self.neg_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def add_positive_percentage(self):
        try:
            value = float(self.pos_entry.get())
            if value <= 0:
                messagebox.showerror("Invalid Input", "Please enter a positive value")
                return
            if value not in self.positive_percentages:
                self.positive_percentages.append(value)
                self.positive_percentages.sort()
                self.update_percentage_lists()
                self.calculate_prices()
                self.save_percentages()
            self.pos_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def remove_negative_percentage(self, value):
        self.negative_percentages.remove(value)
        self.update_percentage_lists()
        self.calculate_prices()
        self.save_percentages()
    
    def remove_positive_percentage(self, value):
        self.positive_percentages.remove(value)
        self.update_percentage_lists()
        self.calculate_prices()
        self.save_percentages()
    
    def restore_defaults(self):
        """Restore the default -10% and +10% values"""
        self.negative_percentages = [-10]
        self.positive_percentages = [10]
        self.update_percentage_lists()
        self.calculate_prices()
        self.save_percentages()
    
    def update_percentage_value(self, old_value, new_value_str, is_negative):
        """Update a percentage value when edited"""
        try:
            new_value = float(new_value_str)
            if is_negative and new_value >= 0:
                new_value = -new_value  # Ensure negative values stay negative
            elif not is_negative and new_value <= 0:
                new_value = abs(new_value)  # Ensure positive values stay positive
                
            if new_value != old_value:
                if is_negative:
                    self.negative_percentages.remove(old_value)
                    self.negative_percentages.append(new_value)
                    self.negative_percentages.sort(reverse=True)
                else:
                    self.positive_percentages.remove(old_value)
                    self.positive_percentages.append(new_value)
                    self.positive_percentages.sort()
                
                self.update_percentage_lists()
                self.calculate_prices()
                self.save_percentages()
        except ValueError:
            # If the input is invalid, revert to the old value
            self.update_percentage_lists()
    
    def update_percentage_lists(self):
        # Clear existing widgets
        for widget in self.neg_list_frame.winfo_children():
            widget.destroy()
        for widget in self.pos_list_frame.winfo_children():
            widget.destroy()
        
        # Add negative percentages
        for value in self.negative_percentages:
            frame = ctk.CTkFrame(self.neg_list_frame)
            frame.pack(fill="x", pady=2)
            
            entry = ctk.CTkEntry(
                frame,
                width=80,
                font=ctk.CTkFont(size=14)
            )
            entry.insert(0, f"{value}")
            entry.pack(side="left", padx=5)
            
            # Add % label
            ctk.CTkLabel(
                frame,
                text="%",
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=(0, 5))
            
            # Bind the entry to update the value when Enter is pressed
            entry.bind('<Return>', lambda e, v=value, ent=entry: self.update_percentage_value(v, ent.get(), True))
            # Also update when focus is lost
            entry.bind('<FocusOut>', lambda e, v=value, ent=entry: self.update_percentage_value(v, ent.get(), True))
            
            ctk.CTkButton(
                frame,
                text="×",
                width=20,
                command=lambda v=value: self.remove_negative_percentage(v)
            ).pack(side="right", padx=5)
        
        # Add positive percentages
        for value in self.positive_percentages:
            frame = ctk.CTkFrame(self.pos_list_frame)
            frame.pack(fill="x", pady=2)
            
            entry = ctk.CTkEntry(
                frame,
                width=80,
                font=ctk.CTkFont(size=14)
            )
            entry.insert(0, f"{value}")
            entry.pack(side="left", padx=5)
            
            # Add % label
            ctk.CTkLabel(
                frame,
                text="%",
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=(0, 5))
            
            # Bind the entry to update the value when Enter is pressed
            entry.bind('<Return>', lambda e, v=value, ent=entry: self.update_percentage_value(v, ent.get(), False))
            # Also update when focus is lost
            entry.bind('<FocusOut>', lambda e, v=value, ent=entry: self.update_percentage_value(v, ent.get(), False))
            
            ctk.CTkButton(
                frame,
                text="×",
                width=20,
                command=lambda v=value: self.remove_positive_percentage(v)
            ).pack(side="right", padx=5)
    
    def calculate_prices(self):
        try:
            fill_price = float(self.fill_price_entry.get())
            
            # Clear existing result labels
            for label in self.result_labels:
                label.destroy()
            self.result_labels.clear()
            
            # Calculate and display negative percentages
            for percentage in self.negative_percentages:
                price = fill_price * (1 + percentage/100)
                label = ctk.CTkLabel(
                    self.results_frame,
                    text=f"{percentage}% Stop Loss: ${price:.2f}",
                    font=ctk.CTkFont(size=16),
                    text_color="#FF4444"
                )
                label.pack(pady=5)
                self.result_labels.append(label)
            
            # Calculate and display positive percentages
            for percentage in self.positive_percentages:
                price = fill_price * (1 + percentage/100)
                label = ctk.CTkLabel(
                    self.results_frame,
                    text=f"+{percentage}% Profit Target: ${price:.2f}",
                    font=ctk.CTkFont(size=16),
                    text_color="#44FF44"
                )
                label.pack(pady=5)
                self.result_labels.append(label)
                
        except ValueError:
            # Clear existing labels
            for label in self.result_labels:
                label.destroy()
            self.result_labels.clear()
            
            # Show error message
            error_label = ctk.CTkLabel(
                self.results_frame,
                text="Please enter a valid number",
                font=ctk.CTkFont(size=16),
                text_color="#FF4444"
            )
            error_label.pack(pady=5)
            self.result_labels.append(error_label)
    
    def clear_all(self):
        """Clear the input field and result labels"""
        self.fill_price_entry.delete(0, tk.END)
        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StockOptionsCalculator()
    app.run() 