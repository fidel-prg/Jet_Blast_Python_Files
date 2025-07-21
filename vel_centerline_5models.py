# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 10:37:05 2025

@author: FIDEL VARGAS
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:49:51 2025
Modified to plot velocity decay for multiple turbulence models
@author: FIDEL VARGAS
"""

import numpy as np
import matplotlib.pyplot as plt
import os


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
D = 1.0  # Jet diameter in meters

base_path = r"C:\Users\FIDEL VARGAS\Desktop\Vel_center"

model_files = {
    "SST k-ω": os.path.join(base_path, "velocity_centerline_kw_SST"),
    "Spalart-Allmaras": os.path.join(base_path, "velocity_centerline_SA"),
    "k-ω GEKO": os.path.join(base_path, "velocity_centerline_GEKO"),
    "k-ε standard": os.path.join(base_path, "velocity_centerline_k_epsilon"),
    "RSM ε-quadratic": os.path.join(base_path, "velocity_centerline_RMS_e_Quadratic")
}


colors = {
    "SST k-ω": "purple",
    "Spalart-Allmaras": "green",
    "k-ω GEKO": "orange",
    "k-ε standard": "blue",
    "RSM ε-quadratic": "red"
}

# === Plotting ===
plt.figure(figsize=(5, 3))

for model, filepath in model_files.items():
    positions, velocities = read_fluent_xy(filepath)
    uj = np.max(velocities)
    xi = positions / D
    uc_uj = velocities / uj

    sorted_indices = np.argsort(xi)
    xi_sorted = xi[sorted_indices]
    uc_uj_sorted = uc_uj[sorted_indices]

    plt.plot(xi_sorted, uc_uj_sorted, label=model, color=colors.get(model, 'black'), linewidth=2)

# Reference flat dotted line from x=0 to x=7
xi_flat = np.linspace(0, 7, 1000)
uc_uj_flat = np.ones_like(xi_flat)
plt.plot(xi_flat, uc_uj_flat, 'k:', linewidth=2)

alpha = 1.4
x_ref = np.linspace(0, 493, 1000)

# Calculate ξ = x / x_c with x_c = 7
xi_shifted = x_ref / 7

# Apply piecewise definition
uc_uj_ref = np.piecewise(
    xi_shifted,
    [xi_shifted <= 1, xi_shifted > 1],
    [lambda xi: 1.0,
     lambda xi: 1 - np.exp(alpha / (1 - xi))]
)

# Prevent numerical overflow: clip to visible range
uc_uj_ref = np.real_if_close(uc_uj_ref)
uc_uj_ref = np.clip(uc_uj_ref, 0, 1)

# Plot the reference dotted line
plt.plot(x_ref, uc_uj_ref, 'k:', linewidth=2, label='Theoretical Model (Lau)')

plt.xlabel(r'$\xi = \dfrac{x}{x_c}$', fontsize=12)
plt.ylabel(r'$\dfrac{u_c}{u_j}$', fontsize=12)
plt.title('Centerline Velocity Decay', fontsize=14)

# Set axis ticks to match reference formatting
plt.xticks(np.arange(0, 550, 50))
plt.yticks(np.arange(0.0, 1.1, 0.1))

plt.legend(fontsize=10, loc='upper right')
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.tight_layout()
plt.show()  



