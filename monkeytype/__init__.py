# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from configparser import ConfigParser
from pathlib import Path
from typing import ContextManager, Optional

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version

from monkeytype.config import Config, get_default_config
from monkeytype.tracing import trace_calls


PACKAGE_NAME = "MonkeyType"


def get_version() -> str:
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        setup_cfg = Path(__file__).resolve().parent.parent / "setup.cfg"
        parser = ConfigParser()
        parser.read(setup_cfg)
        return parser["metadata"]["version"]


__version__ = get_version()


def trace(config: Optional[Config] = None) -> ContextManager[None]:
    """Context manager to trace and log all calls.

    Simple wrapper around `monkeytype.tracing.trace_calls` that uses trace
    logger, code filter, and sample rate from given (or default) config.
    """
    if config is None:
        config = get_default_config()
    return trace_calls(
        logger=config.trace_logger(),
        code_filter=config.code_filter(),
        sample_rate=config.sample_rate(),
        max_typed_dict_size=config.max_typed_dict_size(),
    )
