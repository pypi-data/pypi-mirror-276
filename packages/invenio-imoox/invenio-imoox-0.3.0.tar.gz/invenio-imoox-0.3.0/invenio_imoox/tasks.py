# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks for `invenio-imoox`."""

from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity

from .proxies import current_imoox


@shared_task(ignore_result=True)
def import_imoox_records() -> None:
    """Import imoox records."""
    import_func = current_app.config["IMOOX_IMPORT_FUNC"]

    imoox_service = current_imoox.imoox_rest_service
    records = imoox_service.get_records()

    for record in records:
        try:
            import_func(record, system_identity)
        except RuntimeError as e:
            msg = "ERROR imoox record id: %s couldn't be imported because of %s"
            current_app.logger.error(msg, record["id"], str(e))
