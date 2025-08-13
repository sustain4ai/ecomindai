from fastapi import APIRouter
from src.dto.LLMModelConfig import LLMModelConfig
from src.dto.MLModelConfig import MLModelConfig
from src.dto.InputEstimationLLMInference import InputEstimationLLMInference
from src.dto.InputEstimationML import InputEstimationML
from src.dto.OutputEstimation import OutputEstimation
from src.dto.MLType import MLType
from src.services.serviceLLM.calculation import list_ai_types, launch_estimation_llm_inference, list_llm_model_configs
from typing import List


router = APIRouter()


@router.get("/ai_types")
async def get_ai_types() -> List[str]:
    """
    Récupère les types d'IA pour lesquels EcoMindAI peut faire des estimations
    """
    return list_ai_types()


@router.get("/llm_configurations")
async def get_llm_configurations() -> List[LLMModelConfig]:
    """
    Récupère les configurations disponibles pour un modèle de type LLM
    """
    return list_llm_model_configs()


@router.get("/ml_configurations")
# to change if we choose classification/regression and not ml
async def get_ml_configurations(ml_type: MLType) -> List[MLModelConfig]:
    """
    Récupère les algorithmes disponibles pour un modèle d'IA de machine learning classique de regression ou classification
    """
    return []


@router.post("/estimate_llm_inference")
async def launchEstimationLlm(input_estimation: InputEstimationLLMInference) -> OutputEstimation:
    """
    Lance un calcul d'estimation des métriques d'impacts environnementaux d'un projet LLM sur sa phase d'inférence sur 1 an
    """
    return launch_estimation_llm_inference(input_estimation)


@router.post("/estimate_ml")
async def launchEstimationMl(input_estimation: InputEstimationML) -> OutputEstimation:
    """
    Lance un calcul d'estimation des métriques d'impacts environnementaux d'un projet ML classique sur 1 an
    """
    return OutputEstimation(electricityConsumption=0.0, runtime=0.0, recommendations=[])
