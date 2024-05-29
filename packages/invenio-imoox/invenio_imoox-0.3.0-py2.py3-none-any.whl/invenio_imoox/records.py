# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for `invenio-imoox` module."""

from dataclasses import dataclass

from requests import get


@dataclass
class IMOOXRESTConfig:
    """Imoox rest config."""

    endpoint: str = ""


class IMOOXConnection:
    """Imoox connection."""

    def __init__(self, config: IMOOXRESTConfig) -> None:
        """Construct."""
        self.config = config

    def get(self) -> dict:
        """Get."""
        return get(self.config.endpoint, timeout=10).json()


class IMOOXAPI:
    """Imoox api."""

    connection_cls = IMOOXConnection

    def __init__(self, config: IMOOXRESTConfig) -> None:
        """Construct."""
        self.connection = self.connection_cls(config)

    def get_records(self) -> list[dict]:
        """Get records."""
        return self.connection.get()["data"]
