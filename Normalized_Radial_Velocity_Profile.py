# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 13:11:26 2025

@author: FIDEL VARGAS
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# === USER INPUT ===
filename = "C:/Users/FIDEL VARGAS/Desktop/velocity_proj_u(z)"  # Change this to your actual .xy file
D = 1.0  # Nozzle diameter [m]

# === Function to read Fluent XY data ===
def read_fluent_xy(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    data_lines = []
    for line in lines:
        if line.strip().startswith("((xy/xy/Label") or line.strip().startswith("))"):
            continue
        if line.strip() and not line.startswith("("):
            parts = line.strip().split()
            if len(parts) == 2:
                data_lines.append((float(parts[0]), float(parts[1])))

    data = np.array(data_lines)
    return data[:, 0], data[:, 1]  # position (z), velocity

# === Load and normalize ===
z_positions, w_velocity = read_fluent_xy(filename)
U_c = np.max(w_velocity)
U_Uc = w_velocity / U_c

# Normalize radial coordinate using r_0.5
interpolator = interp1d(U_Uc, z_positions, kind='linear', fill_value='extrapolate')
try:
    r_half = interpolator(0.5)
except:
    print("Warning: U/Uc = 0.5 not found; setting r_half = max(z)")
    r_half = np.max(z_positions)

eta = z_positions / r_half

# === Plot ===
plt.figure(figsize=(3, 3))
plt.plot(eta, U_Uc, label='Simulation k - omega SST', color='blue', linewidth=2)

plt.xlabel(r'$\eta = r / r_{0.5}$', fontsize=14)
plt.ylabel(r'$U/U_c$', fontsize=12)
plt.title('Normalized Radial Velocity Profile', fontsize=14)

plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(0, 3)
plt.ylim(0.0, 1.1)
plt.yticks(np.arange(0.0, 1.01, 0.25))  # <-- Intervals of 0.25

plt.legend(fontsize=7, loc='upper right', frameon=True, labelspacing=0.3, handlelength=0.9)
plt.tight_layout()
plt.show()
