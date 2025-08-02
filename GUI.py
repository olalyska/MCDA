import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def on_radio_change():
    value = radio_var.get()

    if value == "Clear":
        TOPSIS_outer_frame.pack_forget()
    else:
        TOPSIS_outer_frame.pack(padx=10, pady=10, fill="both", expand=True)
        refresh_base_params(value)


def refresh_base_params(method):
    for widget in base_params_frame.winfo_children():
        widget.destroy()
    base_params.clear()

    if method == "TOPSIS":
        fields = ["threshold"]
    elif method == "PROMETHEE":
        fields = ["concordance", "discordance", "dominance", "kernel", "dominated"]
    else:
        fields = []

    for i, label_text in enumerate(fields):
        label = ttk.Label(base_params_frame, text=label_text + ":")
        entry = ttk.Entry(base_params_frame)
        label.grid(row=i, column=0, padx=5, pady=2, sticky="e")
        entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
        base_params[label_text] = entry


def add_attribute():
    index = len(attributes)
    attr_frame = ttk.LabelFrame(attributes_container, text=f"Attribute {index + 1}")
    attr_frame.pack(padx=5, pady=5, fill="x", anchor="n")

    fields = ["step", "min value", "max value", "weight", "criterion (1 or -1)"]
    attr_data = {}

    for i, field in enumerate(fields):
        label = ttk.Label(attr_frame, text=field + ":")
        entry = ttk.Entry(attr_frame, width=10)
        label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)
        attr_data[field] = entry

    attributes.append(attr_data)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def generate_data():
    method = radio_var.get()
    if method == "Clear":
        print("Clear selected. No data to generate.")
        return

    print(f"\n--- Data for method: {method} ---")

    # Base parameters
    print("Base Parameters:")
    for label, entry in base_params.items():
        val = entry.get().strip()
        if is_number(val):
            print(f"  {label}: {float(val)}")
        else:
            print(f"  {label}: INVALID (not a number)")

    # Attributes
    print("Attributes:")
    for i, attr in enumerate(attributes, 1):
        print(f"  Attribute {i}:")
        for label, entry in attr.items():
            val = entry.get().strip()
            if is_number(val):
                print(f"    {label}: {float(val)}")
            else:
                print(f"    {label}: INVALID (not a number)")


root = tk.Tk()
root.title("Decision Method GUI")
root.geometry("400x600")

# Radio buttons
radio_var = tk.StringVar(value="Clear")
radio_frame = ttk.LabelFrame(root, text="Choose Option")
radio_frame.pack(padx=10, pady=10, fill="x")

ttk.Radiobutton(radio_frame, text="TOPSIS", variable=radio_var, value="TOPSIS", command=on_radio_change).pack(
    anchor="w", padx=10, pady=2)
ttk.Radiobutton(radio_frame, text="PROMETHEE I", variable=radio_var, value="PROMETHEE", command=on_radio_change).pack(
    anchor="w", padx=10, pady=2)
ttk.Radiobutton(radio_frame, text="Clear", variable=radio_var, value="Clear", command=on_radio_change).pack(
    anchor="w", padx=10, pady=2)

radio_var = tk.StringVar(value="Clear")
radio_frame = ttk.LabelFrame(root, text="Choose Step")
radio_frame.pack(padx=10, pady=10, fill="x")

ttk.Radiobutton(radio_frame, text="0.01", variable=radio_var, value="0.01", command=on_radio_change).pack(
    anchor="w", padx=10, pady=2)
ttk.Radiobutton(radio_frame, text="0.05", variable=radio_var, value="0.05", command=on_radio_change).pack(
    anchor="w", padx=10, pady=2)
ttk.Radiobutton(radio_frame, text="0.001", variable=radio_var, value="0.001", command=on_radio_change).pack(
    anchor="w", padx=10, pady=2)

# Scrollable area
TOPSIS_outer_frame = ttk.Frame(root)
canvas = tk.Canvas(TOPSIS_outer_frame, borderwidth=0)
scrollbar = ttk.Scrollbar(TOPSIS_outer_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = ttk.Frame(canvas)
scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")


def resize_canvas(event):
    canvas.itemconfig(scrollable_frame_id, width=event.width)


scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", resize_canvas)

# Base Parameters Section
base_params_frame = ttk.LabelFrame(scrollable_frame, text="Base Parameters")
base_params_frame.pack(padx=5, pady=5, fill="x")
base_params = {}

# Attributes Section
attributes_frame = ttk.LabelFrame(scrollable_frame, text="Attributes")
attributes_frame.pack(padx=5, pady=5, fill="x")

attributes_container = ttk.Frame(attributes_frame)
attributes_container.pack(fill="x")

add_attr_btn = ttk.Button(attributes_frame, text="Add Attribute", command=add_attribute)
add_attr_btn.pack(pady=5)

# Generate Button
generate_btn = ttk.Button(scrollable_frame, text="Generate Data", command=generate_data)
generate_btn.pack(pady=10)

attributes = []
on_radio_change()

root.mainloop()
