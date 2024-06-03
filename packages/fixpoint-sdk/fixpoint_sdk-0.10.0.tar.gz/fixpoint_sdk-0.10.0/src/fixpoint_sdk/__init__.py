"""The Fixpoint SDK provides a Python client for the Fixpoint API."""

import fixpoint_openapi as openapi_client

from .client import FixpointClient, ChatRouterClient
from .completions import FixpointChatCompletion, FixpointChatCompletionStream
from . import types
from .types import ThumbsReaction, ModeType
from . import compat
from .lib.logging import logger, LOGGER_NAME

from .lib.exc import FixpointException, InitException, ApiException

__all__ = [
    "FixpointClient",
    "ChatRouterClient",
    "ThumbsReaction",
    "ModeType",
    "openapi_client",
    "types",
    "compat",
    "FixpointChatCompletion",
    "FixpointChatCompletionStream",
    "logger",
    "LOGGER_NAME",
    "FixpointException",
    "InitException",
    "ApiException",
]
