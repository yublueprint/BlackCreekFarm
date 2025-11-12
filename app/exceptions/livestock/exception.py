from ..exception.exception import BaseExceptionParent


class LivestockCreationException(BaseExceptionParent):
    """Raised when creating livestock fails."""
    def __init__(self, message="Failed to create livestock."):
        super().__init__(message)


class LivestockEditException(BaseExceptionParent):
    """Raised when editing livestock fails."""
    def __init__(self, message="Failed to edit livestock."):
        super().__init__(message)


class LivestockDeleteException(BaseExceptionParent):
    """Raised when deleting livestock fails."""
    def __init__(self, message="Failed to delete livestock."):
        super().__init__(message)
