import os
import numpy as np
import matplotlib.pyplot as plt

class OceanThermalVisualizer:
    """
    Generates publication-quality 2D spatial-temporal heatmaps and trajectory plots 
    to visualize directional thermal energy propagation across vertical ocean regimes.
    """
    def __init__(self, output_dir: str = "paper/figures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Configure crisp formatting style sheets for academic output
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.size'] = 11

    def generate_2d_propagation_grid(self, years: list, regimes: list, data_matrix: np.ndarray) -> str:
        """
        Renders a 2D Spatial-Temporal Grid illustrating heat backlog anomalies.
        X-axis: Timeline (Years) | Y-axis: Stratified Fluid Regimes
        """
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
        
        # Render the continuous data plane using an intuitive thermal gradient
        cax = ax.imshow(data_matrix, cmap='YlOrRd', aspect='auto', origin='upper')
        
        # Map explicit categorical ticks matching our physical anchors
        ax.set_xticks(np.arange(len(years)))
        ax.set_xticklabels(years)
        ax.set_yticks(np.arange(len(regimes)))
        ax.set_yticklabels([f"Regime {r}" for r in regimes])
        
        ax.set_title("2D Spatial-Temporal Heat Propagation Anomalies (2020-2025)", weight='bold', pad=15)
        ax.set_xlabel("Timeline (Calendar Years)", labelpad=10)
        ax.set_ylabel("Ocean Stratification Regime", labelpad=10)
        
        # Inject standard metric colorbars calibrated to absolute energy values
        cbar = fig.colorbar(cax, pad=0.02)
        cbar.set_label("Ocean Heat Content Accumulation (ZettaJoules)", labelpad=10)
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, "thermal_propagation_2d.png")
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        print(f"🖼️ Publication figure safely compiled to disk array: {save_path}")
        return save_path

    def plot_ssa_trend(self, years: list, raw_data: np.ndarray, ssa_trend: np.ndarray) -> str:
        """
        Plots the raw empirical time-series against the isolated SSA kinetic trend matrix
        to display non-linear underlying energy directions.
        """
        fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
        
        # Renders the volatile empirical baseline points vs the clean thermodynamic track
        ax.plot(years, raw_data, 'o--', color='gray', alpha=0.6, label='Raw Empirical Observations (Regime C)')
        ax.plot(years, ssa_trend, '-', color='darkred', linewidth=2.5, label='SSA Isolated Long-Term Kinetic Trend')
        
        ax.set_title("Abyssal Regime C Kinetic Energy Trajectory", weight='bold', pad=12)
        ax.set_xlabel("Year", labelpad=8)
        ax.set_ylabel("Heat Content Variance (ZettaJoules)", labelpad=8)
        ax.set_xticks(years)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left', frameon=True)
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, "ssa_abyssal_trend.png")
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        print(f"🖼️ SSA kinetic trajectory plot compiled to disk array: {save_path}")
        return save_path
