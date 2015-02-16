# coding: utf-8


class InvalidZipCodeError(Exception):
    """
    This exception is raised when a invalid or null
    zip code is entered.
    """


class InvalidServiceCodeError(Exception):
    """
    This exception is raised when a invalid service code
    is entered. The service code is provided by Correios.
    """


class InvalidOrderFormatError(Exception):
    """
    This exception is raised when a invalid order format
    is entered. The order format is provided by Correios.
    """
