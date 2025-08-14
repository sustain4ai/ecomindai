from dataclasses import dataclass
from typing import List


@dataclass
class InputData:
    """
    Données d'entrée du calcul d'estimation de l'impact
    """
    mode: str
    project_duration: int
    model_details: str
    parameters_count: str
    framework: str
    quantization: str
    stages: List[str]
    inference_users: int
    inference_requests: int
    inference_tokens: int
    finetuning_data_size: int
    finetuning_epochs_number: int
    finetuning_batch_size: int
    finetuning_peft: str
    infra_type: str
    infra_cpu_cores: int
    infra_gpu_count: int
    infra_gpu_memory: int
    infra_memory: int
    infra_pue_datacenter: float
    infra_pue_machine: float
    location: str
