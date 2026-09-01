"""
OHC regime extraction under the project Methods & Data transparency standard.
"""

from pathlib import Path
from datetime import datetime
import json

class OHCExtractor:
    def __init__(self, data_dir: str = "data"):
        self.raw_dir = Path(data_dir) / "raw"
        self.processed_dir = Path(data_dir) / "processed"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        self.provenance = {
            "extraction_date": datetime.utcnow().isoformat() + "Z",
            "products": {}
        }

    def load_iapv4_ohc(self, filepath: str):
        """Load IAPv4 OHC file. Record exact DOI and access date in provenance."""
        raise NotImplementedError("Implement after first real download")

    def integrate_regimes(self, ds):
        """Compute global OHC for Regime A (0-200m), B (200-2000m), C (>2000m)."""
        raise NotImplementedError("Implement after inspecting actual NetCDF structure")

    def quality_control(self, series):
        """Apply and document basic QC. No silent gap-filling."""
        return series

    def save_processed(self, df, name: str = "iapv4_regimes_ohc.csv"):
        out = self.processed_dir / name
        df.to_csv(out)
        with open(out.with_suffix(".json"), "w") as f:
            json.dump(self.provenance, f, indent=2)
        print(f"Saved: {out}")
