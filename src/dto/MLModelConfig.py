from pydantic import BaseModel, Field


class MLModelConfig(BaseModel):
    """
    Configuration des modèles de machine learning disponibles dans la base
    """
    algorithm_name: str = Field(...,
                                description="Nom de l'algorithme de machine learning utilisé")
