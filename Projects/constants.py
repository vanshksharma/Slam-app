from enum import Enum


class PriorityConstant(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusConstant(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETE = "Complete"