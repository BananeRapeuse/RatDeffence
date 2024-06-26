import tkinter as tk
from tkinter import ttk

def set_styles():
    style = ttk.Style()
    
    # Style for the main frame
    style.configure("TFrame", background="#F0F0F0")
    
    # Style for the buttons
    style.configure("TButton", font=("Helvetica", 12), padding=5)
    
    # Style for the progress bar
    style.configure("TProgressbar", thickness=20)
    
    # Style for the text box
    style.configure("TText", font=("Courier", 10))
