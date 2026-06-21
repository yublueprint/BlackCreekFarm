from ..exception.exception import BaseExceptionParent


class TransactionCreationException(BaseExceptionParent):
    """Raised when creating a transaction fails."""

    def __init__(self, message="Failed to create transaction."):
        super().__init__(message)


class TransactionEditException(BaseExceptionParent):
    """Raised when editing a transaction fails."""

    def __init__(self, message="Failed to edit transaction."):
        super().__init__(message)


class TransactionDeleteException(BaseExceptionParent):
    """Raised when deleting a transaction fails."""

    def __init__(self, message="Failed to delete transaction."):
        super().__init__(message)
