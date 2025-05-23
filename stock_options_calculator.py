import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class StockOptionsCalculator:
    def __init__(self):
        # Set up the main window
        self.root = ctk.CTk()
        self.root.title("Stock Options Calculator")
        self.root.geometry("400x300")
        
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Stock Options Calculator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, pady=10, sticky="ew")
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
        
        # Calculate button
        self.calculate_button = ctk.CTkButton(
            self.main_frame,
            text="Calculate",
            command=self.calculate_prices,
            font=ctk.CTkFont(size=14)
        )
        self.calculate_button.grid(row=2, column=0, pady=20)
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.grid(row=3, column=0, pady=10, sticky="ew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        # Stop loss label
        self.stop_loss_label = ctk.CTkLabel(
            self.results_frame,
            text="",
            font=ctk.CTkFont(size=16),
            text_color="#FF4444"  # Red color for stop loss
        )
        self.stop_loss_label.grid(row=0, column=0, pady=5)
        
        # Profit target label
        self.profit_target_label = ctk.CTkLabel(
            self.results_frame,
            text="",
            font=ctk.CTkFont(size=16),
            text_color="#44FF44"  # Green color for profit target
        )
        self.profit_target_label.grid(row=1, column=0, pady=5)
        
        # Bind Enter key to calculate
        self.fill_price_entry.bind('<Return>', lambda event: self.calculate_prices())
        
    def calculate_prices(self):
        try:
            fill_price = float(self.fill_price_entry.get())
            stop_loss_price = fill_price * 0.9  # -10%
            profit_target_price = fill_price * 1.1  # +10%
            
            self.stop_loss_label.configure(
                text=f"-10% Stop Loss: ${stop_loss_price:.2f}"
            )
            self.profit_target_label.configure(
                text=f"+10% Profit Target: ${profit_target_price:.2f}"
            )
        except ValueError:
            self.stop_loss_label.configure(text="Please enter a valid number")
            self.profit_target_label.configure(text="")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StockOptionsCalculator()
    app.run() 