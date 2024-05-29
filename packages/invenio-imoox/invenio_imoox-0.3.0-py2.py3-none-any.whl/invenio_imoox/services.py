# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for `invenio-imoox` module."""

from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar

from .records import IMOOXAPI, IMOOXRESTConfig


class IMOOXRESTServiceConfig(IMOOXRESTConfig):
    """REST config."""

    api_cls: ClassVar = IMOOXAPI


class IMOOXRESTService:
    """Imoox rest service."""

    def __init__(self, config: IMOOXRESTServiceConfig) -> None:
        """Construct."""
        self._config = config
        self.api = self.api_cls(config=config)

    @property
    def api_cls(self) -> IMOOXAPI:
        """Get api cls."""
        return self._config.api_cls

    def get_records(self) -> list[dict]:
        """Get records."""
        return self.api.get_records()


def build_service(f: Callable) -> Callable:
    """Decorate to build the services."""

    @wraps(f)
    def build(*_: dict, **kwargs: dict) -> Any:  # noqa: ANN401
        endpoint = kwargs.pop("endpoint")
        config = IMOOXRESTServiceConfig(endpoint)
        kwargs["imoox_service"] = IMOOXRESTService(config)

        return f(**kwargs)

    return build
