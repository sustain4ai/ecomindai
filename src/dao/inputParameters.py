"""
Récupère les inputs sur les modèles dont on veut estimer les impacts
"""

from typing import List
import pandas as pd
from src.dto.LLMModelConfig import LLMModelConfig

AI_TYPES = ["LLM", "classification", "regression"]
inputParametersLLMFile = pd.read_csv(
    "./assets/data/input_parameters_llm.csv")


def fetch_llm_model_configs() -> List[LLMModelConfig]:
    """
    Récupère les configurations de LLM dont on est capables d'estimer les impacts
    """
    llm_configs = []
    for _, row in inputParametersLLMFile.iterrows():
        llm_configs.append(LLMModelConfig(modelName=row.model, nbParameters=row.parameters,
                                          framework=row.framework, quantization=row.quantization))
    return llm_configs


def fetch_ai_types() -> List[str]:
    """
    Récupère les types d'IA dont on est capables d'estimer les impacts
    """
    return AI_TYPES
