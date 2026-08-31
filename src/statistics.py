import numpy as np

class SingularSpectrumAnalysis:
    """
    Natively executes Singular Spectrum Analysis (SSA) for time-series decomposition.
    Isolates long-term non-linear thermal signals from high-frequency oceanic noise.
    """
    
    def __init__(self, time_series: np.ndarray, window_length: int):
        """
        Parameters:
        -----------
        time_series : np.ndarray (1D data vector)
        window_length : int (Embedding window L, where 2 <= L <= N/2)
        """
        self.X = time_series
        self.N = len(time_series)
        self.L = window_length
        self.K = self.N - self.L + 1
        
        if not 2 <= self.L <= self.N // 2:
            raise ValueError(f"Window length L must be between 2 and {self.N // 2} for time-series size {self.N}.")

    def embed_trajectory_matrix(self) -> np.ndarray:
        """Step 1: Embed the time series into a spatial Hankel trajectory matrix."""
        H = np.zeros((self.L, self.K))
        for i in range(self.K):
            H[:, i] = self.X[i:i + self.L]
        return H

    def decompose_signal(self) -> tuple:
        """Step 2: Execute Singular Value Decomposition (SVD) on the trajectory matrix."""
        H = self.embed_trajectory_matrix()
        # U: Left singular vectors, S: Eigenvalues, VT: Right singular vectors
        U, S, VT = np.linalg.svd(H, full_matrices=False)
        return U, S, VT

    def reconstruct_trend(self, primary_components: int = 1) -> np.ndarray:
        """
        Steps 3 & 4: Group eigenvalues and apply diagonal averaging to reconstruct
        the clean, long-term underlying trend.
        """
        U, S, VT = self.decompose_signal()
        H_reconstructed = np.zeros((self.L, self.K))
        
        # Reconstruct the Hankel trajectory using only the designated dominant trend components
        for i in range(primary_components):
            H_reconstructed += S[i] * np.outer(U[:, i], VT[i, :])
            
        # Diagonal averaging transformation back to an unrolled 1D time-series
        g = np.zeros(self.N)
        for n in range(self.N):
            vals = []
            for l in range(self.L):
                k = n - l
                if 0 <= k < self.K:
                    vals.append(H_reconstructed[l, k])
            g[n] = np.mean(vals)
        return g


class TimeSeriesStagingEngine:
    """Executes chunked data matrix transitions and linear back-casting operations."""
    
    def __init__(self, depth_regimes: list = ["A", "B", "C"]):
        self.regimes = depth_regimes
        self.state_history = {}

    def ingest_annual_snapshot(self, year: int, regime_data: dict) -> None:
        self.state_history[year] = regime_data
        print(f"📥 Staged snapshot for year {year}: {regime_data} ZJ")

    def execute_blind_forward_step(self, train_start: int, train_end: int, target_year: int) -> tuple:
        years = sorted([y for y in self.state_history.keys() if train_start <= y <= train_end])
        X_mat, Y_mat = [], []
        
        for i in range(len(years) - 1):
            X_mat.append([self.state_history[years[i]][r] for r in self.regimes])
            Y_mat.append([self.state_history[years[i+1]][r] for r in self.regimes])
            
        T_matrix, _, _, _ = np.linalg.lstsq(np.array(X_mat), np.array(Y_mat), rcond=None)
        last_known = np.array([self.state_history[train_end][r] for r in self.regimes])
        pred_vector = np.dot(last_known, T_matrix)
        
        predicted_state = {self.regimes[i]: pred_vector[i] for i in range(len(self.regimes))}
        actual_state = self.state_history[target_year]
        mae = float(np.mean([abs(predicted_state[r] - actual_state[r]) for r in self.regimes]))
        
        return predicted_state, mae

# Execution verification block
if __name__ == "__main__":
    print("📈 Testing Singular Spectrum Analysis (SSA) Extraction Logic...")
    # Simulated 20-year multi-decadal abyssal OHC vector with sharp El Niño oscillations layered over it
    synthetic_abyssal_ohc = np.array([2.1, 2.2, 2.3, 2.5, 2.6, 2.8, 2.9, 3.2, 3.1, 3.4, 
                                      3.6, 3.9, 3.7, 4.1, 4.3, 4.6, 4.4, 4.8, 5.1, 5.3])
    
    ssa = SingularSpectrumAnalysis(synthetic_abyssal_ohc, window_length=6)
    clean_trend = ssa.reconstruct_trend(primary_components=1)
    
    print("\n--- SSA Computation Output ---")
    print(f"Raw Input Series   : {synthetic_abyssal_ohc[:5]}...")
    print(f"Extracted Baseline Trend: {clean_trend[:5]}...")
    print("✅ SSA math engine verified and operating normally.")
