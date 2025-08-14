from typing import List
from pydantic import BaseModel, Field
from src.dto.Recommendation import Recommendation


class OutputEstimation(BaseModel):
    """
    Données de sortie du calcul d'estimation de l'impact : electricité consommée,
    temps et recommandations
    """
    electricityConsumption: float = Field(...,
                                          description="Consommation électrique totale (Wh)")
    runtime: float = Field(..., description="Durée d'exécution totale (s)")
    recommendations: List[Recommendation] = Field(
        ..., description="Liste des recommandations pour réduire l'impact")
