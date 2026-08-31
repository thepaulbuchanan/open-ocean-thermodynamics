import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class TimeSeriesStagingEngine:
    """
    Executes an unbiased, chunked data time-series validation protocol.
    Uses rolling sequential historical blocks (Year N) to project future blocks (Year N+1),
    explicitly calculating spatial and vertical prediction errors to test for baseline falsification.
    """
    
    def __init__(self, depth_regimes: List[str] = ["A", "B", "C"]):
        self.regimes = depth_regimes
        self.state_history: Dict[int, Dict[str, float]] = {}

    def ingest_annual_snapshot(self, year: int, regime_data: Dict[str, float]) -> None:
        """
        Populates the engine with an empirical annual OHC state snapshot.
        
        Parameters:
        -----------
        year : int
            The calendar year of observation.
        regime_data : dict
            Key-value pairs mapping regime ("A", "B", "C") to measured OHC change (in Zettajoules).
        """
        for r in self.regimes:
            if r not in regime_data:
                raise ValueError(f"Missing data payload for Regime {r} in year {year}")
        self.state_history[year] = regime_data
        print(f"📥 Staged snapshot for year {year}: {regime_data} ZJ")

    def compute_empirical_transition_matrix(self, year_start: int, year_end: int) -> np.ndarray:
        """
        Uses classical Markovian/Linear state transitions to determine the back-cast
        advection velocity of heat shifting between vertical ocean regimes without atmospheric models.
        """
        years = sorted([y for y in self.state_history.keys() if year_start <= y <= year_end])
        if len(years) < 2:
            raise ValueError("Insufficient chunk size to compute empirical transition dynamics.")
            
        n_regimes = len(self.regimes)
        X = [] # State vectors at time t
        Y = [] # State vectors at time t+1
        
        for i in range(len(years) - 1):
            t_vector = [self.state_history[years[i]][r] for r in self.regimes]
            t_plus_vector = [self.state_history[years[i+1]][r] for r in self.regimes]
            X.append(t_vector)
            Y.append(t_plus_vector)
            
        # Standard ordinary least squares (OLS) linear inverse matrix solving
        X_arr = np.array(X)
        Y_arr = np.array(Y)
        
        # Solving Y = X * T_matrix -> T_matrix = (X^T * X)^-1 * X^T * Y
        T_matrix, _, _, _ = np.linalg.lstsq(X_arr, Y_arr, rcond=None)
        return T_matrix

    def execute_blind_forward_step(self, train_start: int, train_end: int, target_year: int) -> Tuple[Dict[str, float], float]:
        """
        The Core Falsification Test: Computes a transition matrix on training data blocks,
        steps forward blindly to predict target year OHC, and calculates Mean Absolute Error (MAE).
        """
        if target_year not in self.state_history:
            raise ValueError(f"Target year {target_year} data is missing from phenomenology logs.")
            
        T_matrix = self.compute_empirical_transition_matrix(train_start, train_end)
        
        # Pull the last known state vector from the training matrix window
        last_known_state = np.array([self.state_history[train_end][r] for r in self.regimes])
        
        # Blind matrix dot product step projection
        predicted_state_vector = np.dot(last_known_state, T_matrix)
        predicted_state = {self.regimes[i]: predicted_state_vector[i] for i in range(len(self.regimes))}
        
        # Calculate real-world absolute divergence (Phenomenology vs. Prediction)
        actual_state = self.state_history[target_year]
        errors = [abs(predicted_state[r] - actual_state[r]) for r in self.regimes]
        mae = float(np.mean(errors))
        
        return predicted_state, mae

# Local execution validation verification block
if __name__ == "__main__":
    engine = TimeSeriesStagingEngine()
    print("🤖 Executing verification simulation of the Staging Engine...")
    
    # Simulating fake synthetic multi-year OHC entries to test programmatic plumbing
    # In practice, these will be actual variables derived from NetCDF Argo grids.
    engine.ingest_annual_snapshot(2020, {"A": 8.1, "B": 10.2, "C": 2.1})
    engine.ingest_annual_snapshot(2021, {"A": 8.9, "B": 10.8, "C": 2.2})
    engine.ingest_annual_snapshot(2022, {"A": 12.4, "B": 11.5, "C": 2.3}) # Exploded surface value (Tonga Year)
    engine.ingest_annual_snapshot(2023, {"A": 14.1, "B": 12.1, "C": 2.5})
    
    # Blind projection evaluation block
    # Train on 2020-2022, step forward blindly to guess 2023 values
    pred, error_metric = engine.execute_blind_forward_step(train_start=2020, train_end=2022, target_year=2023)
    
    print("\n🔍 --- Test Results Output ---")
    print(f"Blindly Projected 2023 OHC States: {pred}")
    print(f"Mean Absolute Divergence Error: {error_metric:.4f} ZJ")
    print("✅ Staging Engine plumbing verified and operational.")
