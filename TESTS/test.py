import tkinter as tk
from tkinter import ttk
root = tk.Tk()
frame = tk.Frame(root)
frame.grid()
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

bar = ttk.Progressbar(frame, style="red.Horizontal.TProgressbar", orient="horizontal",
                length=600, mode="determinate", maximum=4, value=1).grid(row=1, column=1)
frame.pack()