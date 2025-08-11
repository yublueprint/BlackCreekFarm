from ..exception.exception import BaseExceptionParent


class EquipmentCreationException(BaseExceptionParent):
    """Raised when creating equipment fails."""

    def __init__(self, message="Failed to create equipment."):
        super().__init__(message)


class EquipmentEditException(BaseExceptionParent):
    """Raised when editing equipment fails."""

    def __init__(self, message="Failed to edit equipment."):
        super().__init__(message)


class EquipmentDeleteException(BaseExceptionParent):
    """Raised when deleting equipment fails."""

    def __init__(self, message="Failed to delete equipment."):
        super().__init__(message)
