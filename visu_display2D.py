import os
import numpy as np
import matplotlib.pyplot as plt
import math

# === CONFIG ===
FOLDER = r"C:\Users\ola72\Documents\magisterka\datasetgenerator\data\TOPSIS_2x"  # <-- CHANGE THIS TO YOUR FOLDER
color_map = {
    0: 'yellow',
    1: 'blue',
    2: 'lime',
    3: 'red'
}

# === Collect valid data files ===
file_list = [f for f in os.listdir(FOLDER) if f.endswith('.csv') or f.endswith('.txt')]
file_list.sort()

# === Prepare subplots ===
num_files = len(file_list)
cols = 5  # Number of columns in the grid
rows = math.ceil(num_files / cols)

fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4), squeeze=False)
fig.suptitle("All Plots (Filtered by y == 0.0)", fontsize=16)

# === Loop through files and plot ===
for idx, filename in enumerate(file_list):
    row = idx // cols
    col = idx % cols
    ax = axes[row][col]

    filepath = os.path.join(FOLDER, filename)
    data = np.loadtxt(filepath, delimiter=",")

    x, y, c = data[:, 0], data[:, 1], data[:, 2].astype(int)

    # Filter where y == 0.0
    x_filtered = x
    y_filtered = y
    c_filtered = c

    # Plot with color grouping
    for color_value in np.unique(c_filtered):
        color_mask = c_filtered == color_value
        ax.scatter(
            x_filtered[color_mask],
            y_filtered[color_mask],
            color=color_map.get(color_value, 'gray'),
            s=7,
            marker="s",
            label=f'Color {color_value}'
        )

    ax.set_title(filename, fontsize=8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(False)

# Hide unused subplots
for i in range(num_files, rows * cols):
    fig.delaxes(axes[i // cols][i % cols])

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()