class InvalidMoveException(Exception):
    """
    Exception raised when an illegal action is performed on a :py:class:`Round`.
    """

    pass


class InvalidOperationException(Exception):
    """
    Exception raised when an operation is performed on a :py:class:`Game`
    when it cannot be performed.
    """

    pass
