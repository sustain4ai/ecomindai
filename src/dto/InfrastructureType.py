from enum import Enum


class InfrastructureType(str, Enum):
    """
    Types d'infrastructures disponibles
    """
    SERVER_DC = "SERVER_DC"
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
