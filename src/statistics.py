# ==============================================================================
# OPEN OCEAN THERMODYNAMICS: PIPELINE ORCHESTRATOR (v2.5 - CAUSALITY CONTROL)
# ==============================================================================
import sys
import os
import shutil
import numpy as np

GITHUB_USER = "thepaulbuchanan"
REPO_NAME = "open-ocean-thermodynamics"
TARGET_DIR = f"/content/{REPO_NAME}"

print("🤖 Initializing Google Colab web runtime context...")
os.chdir("/content")
if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)

print("📥 Executing clean Git repository download...")
!git clone https://github.com

os.chdir(TARGET_DIR)
if TARGET_DIR not in sys.path:
    sys.path.append(TARGET_DIR)

from src.thermodynamics import OceanThermodynamics
from src.data_loader import OceanDataLoader
from src.statistics import TimeSeriesStagingEngine, SingularSpectrumAnalysis, GrangerCausalityTest

def run_advanced_causality_pipeline():
    print("\n🚀 Executing Open Ocean Thermodynamics Inversion Pipeline (v2.5)...\n")
    
    # 1. Initialize data grids
    baseline_curves = {
        2020: {"A": 8.1,  "B": 10.2, "C": 2.1},
        2021: {"A": 8.9,  "B": 10.8, "C": 2.2},
        2022: {"A": 12.4, "B": 11.5, "C": 2.3}, # Tonga Year
        2023: {"A": 14.1, "B": 12.1, "C": 2.5}, # Vapour Traffic Jam Year
        2024: {"A": 15.2, "B": 12.8, "C": 2.6},
        2025: {"A": 14.8, "B": 13.4, "C": 2.8}
    }
    
    # 2. Extract 6-year history vectors for vertical interaction testing
    surface_vector = np.array([baseline_curves[y]["A"] for y in range(2020, 2026)])
    abyssal_vector = np.array([baseline_curves[y]["C"] for y in range(2020, 2026)])
    
    # 3. Execute Granger Causality Tests
    causality_engine = GrangerCausalityTest(lag=1)
    
    # Test Path A: Does the Abyss cause Surface shifts? (Bottom-Up)
    f_stat_bottom_up = causality_engine.evaluate_causality(cause_series=abyssal_vector, effect_series=surface_vector)
    
    # Test Path B: Does the Surface cause Abyssal shifts? (Top-Down)
    f_stat_top_down = causality_engine.evaluate_causality(cause_series=surface_vector, effect_series=abyssal_vector)
    
    print("========================================================")
    print("📋 THERMODYNAMIC INVERSION FRAMEWORK PIPELINE REPORT (v2.5)")
    print("========================================================")
    print(f"Bottom-Up Causality F-Stat (Abyss -> Surface) : {f_stat_bottom_up:.4f}")
    print(f"Top-Down Forcing F-Stat    (Surface -> Abyss) : {f_stat_top_down:.4f}")
    print("--------------------------------------------------------")
    if f_stat_bottom_up > f_stat_top_down:
        print("📊 Physical Interpretation: Directional energy feedback flows from the CRUST upward.")
    else:
        print("📊 Physical Interpretation: Directional energy feedback flows from the ATMOSPHERE downward.")
    print("========================================================")

run_advanced_causality_pipeline()
