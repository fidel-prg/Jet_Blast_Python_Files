# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 11:49:51 2025

@author: FIDEL VARGAS
"""

import numpy as np
import matplotlib.pyplot as plt

# === USER INPUT ===
filename = r"C:\Users\FIDEL VARGAS\Desktop\velocity_centerline.xy"
D = 1.0  # jet diameter in meters

def read_fluent_xy(filename):
    """Reads a Fluent .xy file exported from XY Plot"""
    with open(filename, 'r') as f:
        lines = f.readlines()

    data_lines = []
    for line in lines:
        if line.strip().startswith("((xy/key/label"):
            continue
        if line.strip().startswith(")"):
            break
        if line.strip() and not line.startswith("("):
            parts = line.strip().split()
            if len(parts) == 2:
                data_lines.append((float(parts[0]), float(parts[1])))

    data = np.array(data_lines)
    return data[:, 0], data[:, 1]  # position, velocity

# === USER INPUT ===
filename = "velocity_centerline.xy"  # your Fluent-exported file
D = 1.0  # Jet diameter in meters

# === Load and process ===
positions, velocities = read_fluent_xy(filename)
uj = np.max(velocities)
xi = positions / D
uc_uj = velocities / uj

# Sort for smooth plotting
sorted_indices = np.argsort(xi)
xi_sorted = xi[sorted_indices]
uc_uj_sorted = uc_uj[sorted_indices]

# === Plot ===
plt.figure(figsize=(5, 3))
plt.plot(xi_sorted, uc_uj_sorted, label='SST k-ω (Simulation)', color='purple', linewidth=2)

plt.xlabel(r'$\xi = x / D$', fontsize=12)
plt.ylabel(r'$u_c / u_j$', fontsize=12)
plt.title('Centerline Velocity Decay', fontsize=14)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
