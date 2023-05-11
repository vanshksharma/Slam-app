from enum import Enum


class PriorityConstant(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusConstant(Enum):
    INCOMPLETE = "Incomplete"
    COMPLETE = "Complete"