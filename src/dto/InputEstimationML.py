from pydantic import BaseModel, Field
from src.dto.InfrastructureType import InfrastructureType


class InputEstimationML(BaseModel):
    """
    Données d'entrée du calcul d'estimation de l'impact d'un LLM pour la phase d'inférence
    """
    stage: str = Field(...,
                       description="Etape du cycle de vie de l'IA (entrainement ou inférence ?)")
    algorithmType: str = Field(...,
                               description="Type d'algorithme (classification ou regression)'")
    algorithmName: str = Field(..., description="Nom de l'algorithme")
    nbFeatures: str = Field(...,
                            description="Nombre de features (de colonnes dans le dataset)")
    nbLines: str = Field(
        ..., description="Nombre de lignes dans le dataset correspondant à la stage")
    nbOperations: int = Field(
        ..., description="Nombre d'opérations (d'inférences ou de trainings selon le stage)")
    infrastructureType: InfrastructureType = Field(
        ..., description="Type d'infrastructure utilisée")
    nbCpuCores: int = Field(..., description="Nombre de coeurs de CPU")
    nbGpu: int = Field(..., description="Nombre de GPUs")
    gpuMemory: int = Field(..., description="Taille de la mémoire GPU en Go")
    ramSize: int = Field(..., description="Taille de la RAM en Go")
