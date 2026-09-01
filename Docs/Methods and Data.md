
All results in this study are generated from version-controlled code and publicly available observational products. The complete computational pipeline, intermediate data products, and figure-generation scripts are archived at \url{https://github.com/thepaulbuchanan/open-ocean-thermodynamics} (commit hash recorded at time of submission).


Vertical ocean heat content (OHC) time series are derived from the following primary sources (exact product versions and access dates are recorded in the accompanying repository):


Upper ocean (0--2000m): IAP/CAS gridded OHC product \citep{cheng2024} and/or NOAA/NCEI equivalent, monthly or annual resolution, 2005--present (full Argo coverage era).
   
Deep ocean (>2000m): Deep Argo and GO-SHIP based estimates where available; otherwise explicitly flagged as sparse or unavailable.
 
 Ancillary fields: Argo delayed-mode quality-controlled profiles, GRACE/GRACE-FO ocean mass, and satellite altimetry for steric consistency checks.


No synthetic or hard-coded numerical series are used in the final reported results. Any illustrative or unit-test matrices are clearly labelled as such and excluded from scientific claims.

The global ocean is partitioned into three analysis regimes for diagnostic purposes:

Regime A: 0--200\,m (surface mixed layer)
Regime B: 200--2000\,m (permanent thermocline)
Regime C: $>$2000\,m (abyssal)

These boundaries are operational, not physical impermeable barriers. Vertical exchanges (diapycnal mixing, eddy fluxes, deep convection) are acknowledged and will be examined in subsequent spatial analyses.


Stationarity is assessed via Augmented Dickey--Fuller, KPSS, and Phillips--Perron tests. Cointegration is tested with the Johansen procedure.
Linear directional dependence is evaluated with lag-selected VAR or VECM models. Lag order is chosen by AIC/BIC/HQ; inference uses block-bootstrap or wild-bootstrap methods.
Non-linear and information-theoretic measures (transfer entropy, convergent cross mapping, wavelet coherence) are applied as robustness checks.
All reported test statistics are accompanied by sample size, degrees of freedom, $p$-values (or bootstrap confidence intervals), and sensitivity to lag length.



Exact data product DOIs / snapshot identifiers are recorded.
Processing choices (gap-filling, seasonal cycle removal, trend removal, quality-control flags) are documented in the repository.
Random seeds, bootstrap parameters, and software environment (Python package versions) are fixed and declared.
Intermediate time series used for every published figure and table are archived in the repository.

Any analysis that cannot satisfy the above standards is labelled exploratory or provisional and is not used to support primary claims.