from enum import Enum


class InfrastructureType(str, Enum):
    SERVER_DC = "SERVER_DC"
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
