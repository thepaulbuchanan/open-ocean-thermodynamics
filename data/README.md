# Data Directory

## Structure
- `raw/`     – Original downloaded files (NetCDF, etc.). Not committed to Git (see .gitignore).
- `processed/` – Clean, versioned regime time series (CSV/NetCDF) used in analyses.

## Provenance Rules
Every file placed in `processed/` must have:
1. A corresponding entry in `docs/data_inventory.md`
2. The exact product DOI / version
3. Download / access date
4. Any processing notes

See `docs/Methods_and_Data.md` for the full transparency standard.
