from enum import Enum

class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
    COURIER = "courier"
    COOK = "cook"

class SizeEnum(str, Enum):
    LARGE = "L"
    MEDIUM = "M"
    SMALL = "S"

class OrderStatusEnum(str, Enum):
    CREATED = "created"
    COOKING = "cooking"
    DELIVERING = "delivering"
    DONE = "done"
    CANCELED = "canceled"