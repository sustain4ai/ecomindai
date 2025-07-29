from enum import Enum


class MLType(str, Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
