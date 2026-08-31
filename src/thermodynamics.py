import numpy as np

class OceanThermodynamics:
    """
    Handles inverse-engineering calculations for Ocean Heat Content (OHC) 
    and converts thermal variations into energy flux (W/m²).
    """
    
    def __init__(self, surface_area_global_ocean: float = 3.61e14):
        """
        Parameters:
        -----------
        surface_area_global_ocean : float
            Total surface area of Earth's oceans in square metres. 
            Defaults to standard 3.61 x 10^14 m².
        """
        self.A_ocean = surface_area_global_ocean
        
    @staticmethod
    def calculate_seawater_density(temperature: float, salinity: float) -> float:
        """
        Approximates seawater density (rho) using a simplified linear equation of state.
        For production, this can be swapped with the TEOS-10 standard.
        
        Parameters:
        -----------
        temperature : float (Degrees Celsius)
        salinity : float (Practical Salinity Units - psu)
        """
        # Baseline density parameters
        rho_0 = 1027.0  # kg/m³ reference density
        alpha = 2.0e-4  # Thermal expansion coefficient (1/°C)
        beta = 7.5e-4   # Haline contraction coefficient (1/psu)
        T_0 = 10.0      # Reference temperature (°C)
        S_0 = 35.0      # Reference salinity (psu)
        
        rho = rho_0 * (1.0 - alpha * (temperature - T_0) + beta * (salinity - S_0))
        return float(rho)

    @staticmethod
    def calculate_specific_heat(temperature: float, salinity: float) -> float:
        """
        Calculates specific heat capacity (cp) of seawater in J/(kg*°C).
        Accounts for depression of heat capacity via salinity.
        """
        # Empirical approximation for seawater at nominal ocean pressures
        cp = 4217.4 - 3.7202 * temperature + 0.14128 * (temperature**2) - 7.644 * salinity
        return float(cp)

    def compute_layer_ohc(self, temperature_delta: float, thickness: float, 
                          avg_temperature: float, avg_salinity: float) -> float:
        """
        Calculates the change in Ocean Heat Content (Delta Q) for a specific vertical layer.
        Equation: Delta Q = mass * cp * Delta T
        
        Parameters:
        -----------
        temperature_delta : float
            Observed change in temperature over the time interval (°C)
        thickness : float
            Vertical depth of the layer in metres (e.g., 200.0)
        """
        rho = self.calculate_seawater_density(avg_temperature, avg_salinity)
        cp = self.calculate_specific_heat(avg_temperature, avg_salinity)
        
        # Mass of the layer = Volume * Density
        # Volume = Ocean Surface Area * Layer Thickness
        volume = self.A_ocean * thickness
        mass = volume * rho
        
        # Delta Q in Joules
        delta_q = mass * cp * temperature_delta
        return float(delta_q)

    def convert_energy_to_flux(self, delta_q: float, time_delta_seconds: float) -> float:
        """
        Converts a total Joules energy change into global surface flux (W/m²).
        Equation: F = Delta Q / (Delta t * A_ocean)
        """
        if time_delta_seconds <= 0:
            raise ValueError("Time delta must be greater than zero seconds.")
            
        flux = delta_q / (time_delta_seconds * self.A_ocean)
        return float(flux)

# Quick local test verification block
if __name__ == "__main__":
    calc = OceanThermodynamics()
    print("Testing framework math checks...")
    
    # Test case: 0.01°C warming in a 200m layer over 1 year (31,536,000 seconds)
    dq = calc.compute_layer_ohc(
        temperature_delta=0.01, 
        thickness=200.0, 
        avg_temperature=15.0, 
        avg_salinity=35.0
    )
    flux_output = calc.convert_energy_to_flux(dq, 31536000)
    
    print(f"Calculated Delta Q: {dq:.4e} Joules ({dq / 1e21:.4f} ZettaJoules)")
    print(f"Resulting Global Net Surface Flux: {flux_output:.4f} W/m²")
