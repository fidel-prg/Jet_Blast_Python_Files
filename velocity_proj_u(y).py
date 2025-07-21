# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 10:16:38 2025

@author: FIDEL VARGAS
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 2025

@Author: FIDEL VARGAS
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 2025

@Author: FIDEL VARGAS
"""

import numpy as np
import matplotlib.pyplot as plt

# === USER INPUT ===
filename = "C:/Users/FIDEL VARGAS/Desktop/velocity_proj_u(y)"
D = 1.0  # Jet diameter in meters

def read_fluent_xy(filename):
    """Reads a Fluent .xy file exported from XY Plot"""
    with open(filename, 'r') as f:
        lines = f.readlines()

    data_lines = []
    for line in lines:
        if line.strip().startswith("((xy/xy/label"):
            continue
        if line.strip().startswith("))"):
            break
        if line.strip() and not line.startswith("("):
            parts = line.strip().split()
            if len(parts) == 2:
                data_lines.append((float(parts[0]), float(parts[1])))

    data = np.array(data_lines)
    return data[:, 0], data[:, 1]  # position (y), velocity

# === Load and normalize simulation data ===
positions, velocities = read_fluent_xy(filename)
Uc = np.max(velocities)

zeta = positions / D
U_Uc = velocities / Uc


# === Plot ===
from scipy.interpolate import make_interp_spline

# === Interpolate to smooth the simulation line ===
# Sort the data for interpolation
sorted_indices = np.argsort(U_Uc)
U_Uc_sorted = U_Uc[sorted_indices]
zeta_sorted = zeta[sorted_indices]

# Create a smoother line using spline interpolation
spline = make_interp_spline(U_Uc_sorted, zeta_sorted, k=3)
U_Uc_smooth = np.linspace(U_Uc_sorted.min(), U_Uc_sorted.max(), 300)
zeta_smooth = spline(U_Uc_smooth)

# === Plot ===
plt.figure(figsize=(4, 3))  # Square format like thesis

plt.plot(U_Uc, zeta, label='SST k-$\\omega$ (Simulation)', color='purple', linewidth=2.5)


plt.xlabel('$U/U_c$', fontsize=12)
plt.ylabel('$\\zeta$', fontsize=12)
plt.title('Normalized Vertical Velocity Profile', fontsize=14)

# Axes limits like the thesis figure
plt.xlim(0, 1.05)
plt.ylim(0, 3.5)

plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.legend(loc='upper center', fontsize=10, frameon=False)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()



