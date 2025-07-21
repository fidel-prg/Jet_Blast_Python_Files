import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from scipy.special import erf

# === Verhoff reference curve ===
def verhoff_reference_curve():
    zeta = np.linspace(0.01, 3.5, 300)
    Um_Um0 = 1.48 * zeta**(1/7) * (1 - erf(0.68 * zeta))
    return Um_Um0, zeta

# === Read Fluent-style .xy files ===
def read_fluent_xy(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    data_lines = []
    for line in lines:
        if line.strip() and not line.startswith("("):
            parts = line.strip().split()
            if len(parts) == 2:
                data_lines.append([float(parts[0]), float(parts[1])])
    data = np.array(data_lines)
    return data[:, 0], data[:, 1]  # y, u

# === Normalize using Maslov’s method and shift so wall is at y=0 ===
def normalize_profile(y, u):
    y_shifted = y - np.min(y)  # Shift so wall starts at 0
    u_max = np.max(u)
    u_norm = u / u_max
    half_u = 0.5 * u_max
    idx_half = np.argmin(np.abs(u - half_u))
    By = y_shifted[idx_half]
    y_norm = y_shifted / By
    return y_norm, u_norm

# === File Paths ===
base_path = r"C:\Users\FIDEL VARGAS\Desktop\Vel_proj_u(y)"

model_files = {
    'SST k-$\omega$': os.path.join(base_path, "velocity_proj_u(y)_k_w_SST"),
    'Spalart-Allmaras': os.path.join(base_path, "velocity_proj_u(y)_SA"),
    'k-$\omega$ GEKO': os.path.join(base_path, "velocity_proj_u(y)_GEKO"),
    'k-$\epsilon$ standard': os.path.join(base_path, "velocity_proj_u(y)_k_epsilon"),
    'RSM $\epsilon$-quadratic': os.path.join(base_path, "velocity_proj_u(y)_RSM"),
}

colors = {
    'SST k-$\omega$': 'purple',
    'Spalart-Allmaras': 'green',
    'k-$\omega$ GEKO': 'orange',
    'k-$\epsilon$ standard': 'blue',
    'RSM $\epsilon$-quadratic': 'red'
}

# === Plotting ===
plt.figure(figsize=(4, 3))

for label, filepath in model_files.items():
    y, u = read_fluent_xy(filepath)
    y_norm, u_norm = normalize_profile(y, u)

    # Sort data for interpolation
    sort_idx = np.argsort(y_norm)
    y_sorted = y_norm[sort_idx]
    u_sorted = u_norm[sort_idx]

    # Apply safe monotonic interpolation (no overshoot)
    pchip = PchipInterpolator(y_sorted, u_sorted)
    y_smooth = np.linspace(y_sorted.min(), y_sorted.max(), 300)
    u_smooth = pchip(y_smooth)

    plt.plot(u_smooth, y_smooth, label=label, color=colors[label])

# === Add Verhoff Reference ===
ref_u, ref_y = verhoff_reference_curve()
plt.plot(ref_u, ref_y, 'k--', label='Verhoff Reference')

# === Final plot formatting ===
plt.xlabel(r'$U/U_{max}$')
plt.ylabel(r'$Y/B_y$')
plt.title('Normalized Axial Velocity Profiles of Turbulence Models')
plt.grid(True)
plt.legend()
plt.ylim([0, 3.5])
plt.xlim([0, 1.05])
plt.tight_layout()
plt.show()

