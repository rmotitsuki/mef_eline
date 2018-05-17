"""MEF Eline Exceptions."""


class MEFELineException(Exception):
    """MEF Eline Base Exception."""

    def __init__(self, message):
        """Constructor of MEFELineException."""
        super().__init__(message)


class EVCException(MEFELineException):
    """EVC Exception."""

    def __init__(self, message):
        """Constructor of EVCException."""
        super().__init__(message)


class ValidationException(EVCException):
    """Exception for validation errors."""

    def __init__(self, message):
        """Constructor of ValidationException."""
        super().__init__(message)
