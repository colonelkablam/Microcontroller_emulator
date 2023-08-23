from enum import Enum
# locally used enums for pin direction/values
class PinDir(Enum):
    INPUT = 1
    OUTPUT = 0

class PinVal(Enum):
    ON = 1
    OFF = 0

class Side(Enum):
    LEFT = 0
    RIGHT = 1