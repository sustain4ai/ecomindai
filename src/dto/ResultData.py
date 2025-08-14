from dataclasses import dataclass
from matplotlib.figure import Figure


@dataclass
class ResultData:
    """
    Données de sortie du calcul d'estimation de l'impact
    """
    energy_consumption: str
    carbon_footprint: str
    abiotic_resource_usage: str
    water_usage: str
    eq_energy_consumption: str
    eq_carbon_footprint: str
    eq_abiotic_resources: str
    eq_water_usage: str
    carbon_footprint_chart: Figure
    abiotic_resource_chart: Figure
    water_usage_chart: Figure
    more_frugal_conf: str
    percentage_reduction: str
