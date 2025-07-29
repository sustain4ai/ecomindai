import pandas as pd
from typing import List
from src.dto.LLMModelConfig import LLMModelConfig

AI_TYPES = ["LLM", "classification", "regression"]
inputParametersLLMFile = pd.read_csv(
    "./assets/data/input_parameters_llm.csv")


def fetch_llm_model_configs() -> List[LLMModelConfig]:
    llm_configs = []
    for _, row in inputParametersLLMFile.iterrows():
        llm_configs.append(LLMModelConfig(modelName=row.model, nbParameters=row.parameters,
                                          framework=row.framework, quantization=row.quantization))
    return llm_configs


def fetch_ai_types() -> List[str]:
    return AI_TYPES
