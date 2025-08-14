from pydantic import BaseModel, Field


class LLMModelConfig(BaseModel):
    """
    Configuration de LLM disponibles dans la base
    """
    modelName: str = Field(description="Nom du modèle LLM utilisé")
    nbParameters: str = Field(
        description="Nombre de paramètres (en milliards)")
    framework: str = Field(description="Nom du modèle utilisé")
    quantization: str = Field(
        description="Méthode de quantization utilisée (none si pas de quantization)")
