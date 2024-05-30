from __future__ import annotations

import sh
import typing


class PytestTFException(Exception):
    """Base exception for pytest-tf."""


class TFError(PytestTFException):
    """Base error for pytest-tf."""


class InvalidTFRunner(TFError):
    """Error raised when an invalid runner is provided."""

    def __init__(self, runner: str):
        self.runner = runner
        super().__init__(f"Invalid TF runner: {runner}")


class TFRuntimeError(TFError, RuntimeError):
    """Error raised when a runtime error occurs."""

    STAGE: str = ""

    def __init__(self, message: str, **kwargs):
        """Initializes the error with a message."""

        self.message = message
        if self.STAGE:
            super().__init__(f"TF Error during {self.STAGE}: {self.message} {kwargs}")
        else:
            super().__init__(f"TF Error at runtime: {self.message} {kwargs}")

    @classmethod
    def from_sh_error(cls, error: sh.ErrorReturnCode, **kwargs) -> TFRuntimeError:
        """Creates an instance of the error from a sh error. Does this by trying
        to determine the error type from the message, then calling the appropriate
        constructor."""

        message = "\n" + error.stderr.decode("utf-8")

        if NoTFConfiguration._should_capture(message):
            return NoTFConfiguration._from_sh_error(error, **kwargs)

        return cls._from_sh_error(error, **kwargs)

    @classmethod
    def _from_sh_error(cls, error: sh.ErrorReturnCode, **kwargs) -> typing.Self:
        """All children inherit this method. It creates an instance of the error
        by just capturing the message from the error."""

        message = error.stderr.decode("utf-8")
        return cls(message, **kwargs)

    @classmethod
    def _should_capture(cls, message: str) -> bool:
        """Determines if the error should be captured by this class. All
        children should override this method."""
        return False


class TFInitError(TFRuntimeError):
    """Error raised when an error occurs during tf init."""

    STAGE = "init"


class TFPlanError(TFRuntimeError):
    """Error raised when an error occurs during tf plan."""

    STAGE = "plan"


class TFApplyError(TFRuntimeError):
    """Error raised when an error occurs during tf apply."""

    STAGE = "apply"


class TFDestroyError(TFRuntimeError):
    """Error raised when an error occurs during tf destroy."""

    STAGE = "destroy"


###### INIT ERRORS #########

###### PLAN ERRORS #########


class NoTFConfiguration(TFPlanError):
    """Error raised when no tf configuration is found."""

    def __init__(self, _, **kwargs):
        """Captures the path to the configuration, then calls the super constructor."""
        path = kwargs.pop("path")

        if path:
            super().__init__(f"No TF configuration found at {path}", **kwargs)
        else:
            super().__init__("No TF configuration found", **kwargs)

    @classmethod
    def _should_capture(cls, message: str) -> bool:
        return "No configuration files" in message


###### APPLY ERRORS ########

###### DESTROY ERRORS ######
