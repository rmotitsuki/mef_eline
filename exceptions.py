"""MEF Eline Exceptions."""


class MEFELineException(Exception):
    """MEF Eline Base Exception."""


class EVCException(MEFELineException):
    """EVC Exception."""


class ValidationException(EVCException):
    """Exception for validation errors."""
