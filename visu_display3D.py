import os
import numpy as np
import matplotlib.pyplot as plt
import math

# === CONFIG ===
FOLDER = r"C:\Users\ola72\Documents\magisterka\datasetgenerator\data"  # <-- CHANGE THIS TO YOUR FOLDER
color_map = {
    0: 'black',
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

    x, y, z, c = data[:, 0], data[:, 1], data[:, 2], data[:, 3].astype(int)

    # Filter where y == 0.0
    mask = y == 0.5
    x_filtered = x[mask]
    z_filtered = z[mask]
    c_filtered = c[mask]

    # Plot with color grouping
    for color_value in np.unique(c_filtered):
        color_mask = c_filtered == color_value
        ax.scatter(
            x_filtered[color_mask],
            z_filtered[color_mask],
            color=color_map.get(color_value, 'gray'),
            s=5,
            label=f'Color {color_value}'
        )

    ax.set_title(filename, fontsize=8)
    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.grid(True)

# Hide unused subplots
for i in range(num_files, rows * cols):
    fig.delaxes(axes[i // cols][i % cols])

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()