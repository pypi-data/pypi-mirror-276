__version__ = "2.0.0"
# from . import longest
from inspect import getmembers
from inspect import isfunction

from ._api_compat import input
from ._api_compat import output
from ._api_compat import run
from ._api_compat import run_async
from .FilterGraph import Stream
from .filters import *  # noqa: F403 this is impossible to avoid
from .generated_filters import *  # noqa: F403 this is impossible to avoid
from .probe import probe
from .view import view

# This is for `from xyz import *`, but also to make linter shut up

__all__ = ["input", "output", "run", "run_async", "probe", "view", "generated_filters", "filters"]  # noqa: F405

stream_modules = [generated_filters, _api_compat]  # noqa: F405

for module in stream_modules:
    for name, func in getmembers(module, isfunction):
        setattr(Stream, name, func)
