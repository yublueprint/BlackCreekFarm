from ..exception.exception import BaseExceptionParent


class CropCreationException(BaseExceptionParent):
    """Raised when creating a crop fails."""

    def __init__(self, message="Failed to create crop."):
        super().__init__(message)


class CropEditException(BaseExceptionParent):
    """Raised when editing a crop fails."""

    def __init__(self, message="Failed to edit crop."):
        super().__init__(message)


class CropDeleteException(BaseExceptionParent):
    """Raised when deleting a crop fails."""

    def __init__(self, message="Failed to delete crop."):
        super().__init__(message)
