from enum import Enum


class MLType(str, Enum):
    """
    Type d'algorithmes de machines learning pour lesquels on peut estimer l'impact
    """
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
