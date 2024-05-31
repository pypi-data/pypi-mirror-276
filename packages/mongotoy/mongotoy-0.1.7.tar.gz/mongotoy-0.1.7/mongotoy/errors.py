import typing
from typing import Union


class ErrorWrapper:
    # noinspection SpellCheckingInspection
    """
        Wrapper class for handling errors in the mongotoy library.

        Args:
            error (Exception): The wrapped error instance.
            loc (str): The location where the error occurred.

        Raises:
            TypeError: If `loc` is not a tuple of strings.
        """

    def __init__(self, error: Union[Exception, 'ErrorWrapper'], loc: tuple[str] = tuple()):
        self._loc, self._error = self._unwrap_error(loc, error)

    def _unwrap_error(self, loc: tuple[str], error: Exception) -> tuple[tuple[str], Exception]:
        """
        Recursively unwrap nested ErrorWrapper instances to get the original error and its location.

        Parameters:
            loc (tuple[str]): The current location information.
            error (Exception): The wrapped error instance.

        Returns:
            tuple[tuple[str], Exception]: The final location information and the original error.
        """
        if isinstance(error, ErrorWrapper):
            # noinspection PyTypeChecker
            return self._unwrap_error(loc + error.loc, error.error)
        return loc, error

    @property
    def loc(self) -> tuple[str]:
        """
        Get the location where the error occurred.

        Returns:
            tuple[str]: The location represented as a tuple of strings.
        """
        return self._loc

    @property
    def error(self) -> Exception:
        """
        Get the wrapped error instance.

        Returns:
            Exception: The wrapped error instance.
        """
        return self._error

    def get_message(self) -> str:
        """
        Get the formatted error message.

        Returns:
            str: The formatted error message.
        """
        return f'{".".join(self.loc)} -> {str(self.error)}'

    def dump_json(self) -> dict:
        """
        Convert the error information to a valid json.

        Returns:
            dict: A json valid containing the location and string representation of the error.
        """
        return {
            'type': self.error.__class__.__name__,
            'loc': list(self.loc),
            'error': str(self.error)
        }


class ValidationError(Exception):
    # noinspection SpellCheckingInspection
    """
        Exception class to represent data validation errors in the mongotoy library.

        Args:
            *errors (ErrorWrapper): List of ErrorWrapper instances containing details of validation errors.

        Raises:
            TypeError: If `errors` is not a list of ErrorWrapper instances.
        """

    def __init__(self, *errors: ErrorWrapper):
        if not all(isinstance(e, ErrorWrapper) for e in errors):
            raise TypeError("Errors must be a list of ErrorWrapper instances.")

        self._errors = errors
        super().__init__(self._get_message())

    def _get_message(self) -> str:
        """
        Get the error message for the validation exception.

        Returns:
            str: The error message indicating the number of invalid fields.
        """
        msg = f'Invalid data at:'
        for err in self.errors:
            msg += f'\n  * {err.get_message()}'
        return msg

    @property
    def errors(self) -> list[ErrorWrapper]:
        """
        Get the list of validation errors.

        Returns:
            list[ErrorWrapper]: List of ErrorWrapper instances representing validation errors.
        """
        return list(self._errors)

    def dump_json(self) -> dict:
        """
        Convert the validation error information to a valid json.

        Returns:
            dict: A json valid containing the details of validation errors.
        """
        return {
            'type': 'ValidationError',
            'errors': [e.dump_json() for e in self.errors]
        }


class DocumentValidationError(ValidationError):
    # noinspection SpellCheckingInspection
    """
        Exception class to represent data validation errors at documents in the mongotoy library.

        Args:
            document_cls (typing.Type): The type of document where the validation error occurred.
            errors (list[ErrorWrapper]): List of ErrorWrapper instances containing details of validation errors.
        """

    def __init__(self, document_cls: typing.Type, errors: list[ErrorWrapper]):
        self._document_cls = document_cls
        super().__init__(*errors)

    def _get_message(self) -> str:
        """
        Get the error message for the document validation exception.

        Returns:
            str: The error message indicating the invalid fields.
        """
        msg = f'Invalid data at:'
        for err in self.errors:
            msg += f'\n  * {ErrorWrapper(error=err, loc=(self._document_cls.__name__,)).get_message()}'
        return msg

    def dump_json(self) -> dict:
        """
        Convert the document validation error information to a valid json.

        Returns:
            dict: A json valid containing the details of document validation errors.
        """
        return {
            'type': 'DocumentValidationError',
            'document': self._document_cls.__name__,
            'errors': super().dump_json()['errors']
        }


class DocumentError(Exception):
    # noinspection SpellCheckingInspection
    """
        Exception class to represent errors related to document definitions in the mongotoy library.

        Args:
            loc (tuple[str]): The location where the error occurred.
            msg (str): The error message.
        """

    def __init__(self, loc: tuple[str], msg: str):
        super().__init__(f'[{".".join(loc)}]. {msg}')


class EngineError(Exception):
    """
    Error raised for engine-related issues.

    This exception is raised when there are errors related to engine operations

    """


class SessionError(Exception):
    """
    Error raised for session-related issues.

    This exception is raised when there are errors related to session operations

    """


class NoResultError(Exception):
    """
    Error raised when no results are found.

    This exception is raised when an operation expects a result, but none are found.

    """
