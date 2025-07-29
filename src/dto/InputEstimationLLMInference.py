
from pydantic import BaseModel, Field
from src.dto.InfrastructureType import InfrastructureType


class InputEstimationLLMInference(BaseModel):
    """
    Données d'entrée du calcul d'estimation de l'impact d'un LLM pour la phase d'inférence
    """
    modelName: str = Field(..., description="Nom du modèle LLM")
    nbParameters: str = Field(...,
                              description="Nombre de paramètres (en milliards)")
    framework: str = Field(..., description="Nom du modèle utilisé")
    quantization: str = Field(
        ..., description="Méthode de quantization utilisée (none si pas de quantization)")
    totalGeneratedTokens: int = Field(...,
                                      description="Nombre de tokens générés sur un an")
    infrastructureType: InfrastructureType = Field(
        ..., description="Type d'infrastructure utilisée")
    nbCpuCores: int = Field(..., description="Nombre de coeurs de CPU")
    nbGpu: int = Field(..., description="Nombre de GPUs")
    gpuMemory: int = Field(..., description="Taille de la mémoire GPU en Go")
    ramSize: int = Field(..., description="Taille de la RAM en Go")
