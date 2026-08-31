import os
import numpy as np
import matplotlib.pyplot as plt

# Standard style configurations
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
os.makedirs("paper/figures", exist_ok=True)

years = [2020, 2021, 2022, 2023, 2024, 2025]
data_matrix = np.array([
    [8.1,  8.9,  12.4, 14.1, 15.2, 14.8],
    [10.2, 10.8, 11.5, 12.1, 12.8, 13.4],
    [2.1,  2.2,  2.3,  2.5,  2.6,  2.8]
])

# Generate Figure 1: Spatial Grid Matrix
fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
cax = ax.imshow(data_matrix, cmap='YlOrRd', aspect='auto')
ax.set_xticks(np.arange(len(years)))
ax.set_xticklabels(years)
ax.set_yticks(np.arange(3))
ax.set_yticklabels(["Regime A", "Regime B", "Regime C"])
ax.set_title("2D Spatial-Temporal Ocean Heat Propagation", weight='bold', pad=10)
fig.colorbar(cax, label="Ocean Heat Content Accumulation (ZettaJoules)")
plt.tight_layout()
plt.savefig("paper/figures/thermal_propagation_2d.png", bbox_inches='tight')
plt.close()

print("🖼️ Production graphics compiled directly to paper/figures/.")
