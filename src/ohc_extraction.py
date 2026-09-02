"""
OHC regime extraction for IAPv4 monthly files.
Complies with project Methods & Data transparency standard.
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import re
import numpy as np
import pandas as pd
from netCDF4 import Dataset


class OHCExtractor:
    def __init__(self, data_dir: str = "data"):
        self.raw_dir = Path(data_dir) / "raw" / "iapv4"
        self.processed_dir = Path(data_dir) / "processed"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        self.provenance = {
            "extraction_date": datetime.now(timezone.utc).isoformat(),
            "product": "IAPv4 Ocean Heat Content (Cheng et al.)",
            "doi": "10.12157/IOCAS.20240117.001",
            "source_url": "http://www.ocean.iap.ac.cn/ftp/cheng/IAPv4_IAP_Temperature_gridded_1month_netcdf/",
            "baseline": "1981-2010",
            "units_raw": "J/m^2",
            "variables_used": {},
            "notes": []
        }

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _earth_grid_areas(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
        """
        Approximate grid-cell areas (m²) for a regular 1° lat-lon grid.
        Uses spherical Earth, R = 6371e3 m.
        Returns 2-D array (nlat, nlon).
        """
        R = 6371e3
        dlat = np.deg2rad(1.0)
        dlon = np.deg2rad(1.0)
        lat_rad = np.deg2rad(lat)
        # area of each latitude band
        area_per_lon = R**2 * dlon * (np.sin(lat_rad + dlat/2) - np.sin(lat_rad - dlat/2))
        areas = np.tile(area_per_lon[:, np.newaxis], (1, len(lon)))
        return areas

    def _global_integral_zj(self, field: np.ndarray, lat: np.ndarray, lon: np.ndarray) -> float:
        """
        Convert a 2-D OHC field (J/m²) to global integral in ZettaJoules.
        Handles NaN / fill values.
        """
        areas = self._earth_grid_areas(lat, lon)
        # Mask invalid
        valid = np.isfinite(field) & (np.abs(field) < 1e29)
        total_joules = np.nansum(field[valid] * areas[valid])
        return float(total_joules / 1e21)  # J → ZJ

    # ------------------------------------------------------------------
    # Single-file processing
    # ------------------------------------------------------------------
    def process_monthly_file(self, filepath: Path) -> dict:
        """
        Read one IAPv4 monthly NetCDF and return regime integrals (ZJ).
        """
        with Dataset(filepath, "r") as ds:
            lat = ds.variables["lat"][:]
            lon = ds.variables["lon"][:]
            time_val = float(ds.variables["time"][0])  # yyyymm

            year = int(time_val // 100)
            month = int(time_val % 100)

            # Load the layers we need
            ohc100  = np.array(ds.variables["OHC100"][:], dtype=float)
            ohc300  = np.array(ds.variables["OHC300"][:], dtype=float)
            ohc2000 = np.array(ds.variables["OHC2000"][:], dtype=float)
            ohc6000 = np.array(ds.variables["OHC6000"][:], dtype=float)

            # Replace fill value
            fill = 1.0e30
            for arr in (ohc100, ohc300, ohc2000, ohc6000):
                arr[np.abs(arr) >= fill * 0.9] = np.nan

            # Global integrals (ZJ)
            a100  = self._global_integral_zj(ohc100,  lat, lon)
            a300  = self._global_integral_zj(ohc300,  lat, lon)
            a2000 = self._global_integral_zj(ohc2000, lat, lon)
            a6000 = self._global_integral_zj(ohc6000, lat, lon)

            # Regime definitions (transparent approximations)
            # Regime A (0-200 m): linear interpolation between 100 m and 300 m
            regime_a = a100 + (a300 - a100) * (200 - 100) / (300 - 100)

            # Regime B (200-2000 m)
            regime_b = a2000 - regime_a

            # Regime C (>2000 m)
            regime_c = a6000 - a2000

            result = {
                "year": year,
                "month": month,
                "date": f"{year:04d}-{month:02d}",
                "regime_a_zj": regime_a,
                "regime_b_zj": regime_b,
                "regime_c_zj": regime_c,
                "ohc100_zj": a100,
                "ohc300_zj": a300,
                "ohc2000_zj": a2000,
                "ohc6000_zj": a6000,
            }
            return result

    # ------------------------------------------------------------------
    # Batch processing
    # ------------------------------------------------------------------
    def process_directory(self, pattern: str = "*.nc") -> pd.DataFrame:
        """
        Process all matching NetCDF files in data/raw/iapv4/.
        Returns a sorted DataFrame of monthly regime time series.
        """
        files = sorted(self.raw_dir.glob(pattern))
        if not files:
            raise FileNotFoundError(f"No files matching {pattern} in {self.raw_dir}")

        records = []
        for f in files:
            try:
                rec = self.process_monthly_file(f)
                records.append(rec)
                print(f"✓ {f.name} → {rec['date']}")
            except Exception as e:
                print(f"✗ {f.name}: {e}")
                self.provenance["notes"].append(f"Failed: {f.name} – {e}")

        df = pd.DataFrame(records)
        df = df.sort_values(["year", "month"]).reset_index(drop=True)

        # Record variables used
        self.provenance["variables_used"] = {
            "regime_a": "linear interpolation of OHC100 and OHC300 to 200 m",
            "regime_b": "OHC2000 - regime_a",
            "regime_c": "OHC6000 - OHC2000",
            "raw_layers": ["OHC100", "OHC300", "OHC2000", "OHC6000"]
        }
        self.provenance["n_files"] = len(files)
        self.provenance["time_range"] = f"{df['date'].iloc[0]} to {df['date'].iloc[-1]}" if len(df) else "empty"

        return df

    def save(self, df: pd.DataFrame, name: str = "iapv4_regimes_monthly.csv"):
        out_csv = self.processed_dir / name
        out_json = out_csv.with_suffix(".json")

        df.to_csv(out_csv, index=False)
        with open(out_json, "w") as f:
            json.dump(self.provenance, f, indent=2)

        print(f"\nSaved time series → {out_csv}")
        print(f"Saved provenance  → {out_json}")
        return out_csv


# ------------------------------------------------------------------
# Convenience CLI
# ------------------------------------------------------------------
if __name__ == "__main__":
    extractor = OHCExtractor(data_dir="data")
    df = extractor.process_directory("*.nc")
    print("\nPreview:")
    print(df.head(12))
    print("...")
    print(df.tail(6))
    extractor.save(df)