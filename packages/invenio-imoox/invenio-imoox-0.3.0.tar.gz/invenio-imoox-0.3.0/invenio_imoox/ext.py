# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Provides API for iMooX."""

from flask import Flask

from . import config
from .services import IMOOXRESTService, IMOOXRESTServiceConfig


class InvenioIMooX:
    """invenio-imoox extension."""

    def __init__(self, app: Flask = None) -> None:
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        app.extensions["invenio-imoox"] = self

    def init_config(self, app: Flask) -> None:
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("INVENIO_IMOOX_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app: Flask) -> None:
        """Init services."""
        endpoint = app.config.get("IMOOX_ENDPOINT", "")
        config = IMOOXRESTServiceConfig(endpoint)
        self.imoox_rest_service = IMOOXRESTService(config)
