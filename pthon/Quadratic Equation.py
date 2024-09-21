import math
import tkinter as tk
from tkinter import messagebox

def calculate_roots():
    a = float(entry_a.get())
    b = float(entry_b.get())
    c = float(entry_c.get())

    # Finding Discriminant
    D = b**2 - 4*a*c

    sqrt_val = math.sqrt(abs(D))

    if D > 0:
        root1 = (-b + sqrt_val) / (2 * a)
        root2 = (-b - sqrt_val) / (2 * a)
        result_label.config(text=f"Roots are real and unequal:\nRoot 1: {round(root1, 3)}\nRoot 2: {round(root2, 3)}")
    elif D == 0:
        root = -b / (2 * a)
        result_label.config(text=f"Roots are real and equal:\nRoot: {round(root, 3)}")
    else:
        result_label.config(text="Roots are unreal and unequal. Cannot be calculated.")

# Create the GUI
root = tk.Tk()
root.title("Quadratic Equation Solver")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

entry_a = tk.Entry(frame, width=10)
entry_a.grid(row=0, column=0, padx=5, pady=5)
label_a = tk.Label(frame, text="x^2 +")
label_a.grid(row=0, column=1, padx=5, pady=5)

entry_b = tk.Entry(frame, width=10)
entry_b.grid(row=0, column=2, padx=5, pady=5)
label_b = tk.Label(frame, text="x +")
label_b.grid(row=0, column=3, padx=5, pady=5)

entry_c = tk.Entry(frame, width=10)
entry_c.grid(row=0, column=4, padx=5, pady=5)
label_c = tk.Label(frame, text="= 0")
label_c.grid(row=0, column=5, padx=5, pady=5)

calculate_button = tk.Button(frame, text="Calculate Roots", command=calculate_roots)
calculate_button.grid(row=1, column=0, columnspan=6, padx=5, pady=10)

result_label = tk.Label(frame, text="", font=("Arial", 12))
result_label.grid(row=2, column=0, columnspan=6, padx=5, pady=10)

root.mainloop()

