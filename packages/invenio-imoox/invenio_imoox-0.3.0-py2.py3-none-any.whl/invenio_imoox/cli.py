# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for `invenio-imoox` module."""

import re

from click import STRING, group, option, secho
from flask import current_app
from flask.cli import with_appcontext
from invenio_access.permissions import any_user
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts

from .services import IMOOXRESTService, build_service


class RegexEqual(str):
    """Regex equal to use regex in match case."""

    __slots__ = ()

    def __eq__(self, pattern: str) -> bool:
        """Override == operator."""
        return bool(re.search(pattern, self))


@group()
def imoox() -> None:
    """CLI-group for `invenio-imoox` commands."""


@imoox.command("import")
@with_appcontext
@option("--endpoint", required=True)
@option("--user-email", type=STRING)
@option("--dry-run", is_flag=True, default=False)
@build_service
def import_from_imoox(
    imoox_service: IMOOXRESTService,
    user_email: str,
    *,
    dry_run: bool,
) -> None:
    """Import metadata from endpoint into the repository."""
    try:
        user = current_accounts.datastore.get_user_by_email(user_email)
        identity = get_identity(user)
        identity.provides.add(any_user)
    except AttributeError:
        secho("The given user has not been found in the database", fg="red")
        return

    import_func = current_app.config.get("IMOOX_REPOSITORY_IMPORT_FUNC")
    records = imoox_service.get_records()

    for imoox_record in records:
        try:
            record = import_func(imoox_record, identity, dry_run=dry_run)
            secho(f"successfully created record: {record.id}", fg="green")
        except RuntimeError as error:
            match RegexEqual(str(error)):
                case "DRY_RUN.*success":
                    secho(str(error), fg="green")
                case "DRY_RUN.*error":
                    secho(str(error), fg="magenta")
                case _:
                    secho(str(error), fg="red")
