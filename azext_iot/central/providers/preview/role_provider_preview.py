# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from typing import List
from azext_iot.central.models.rolePreview import RolePreview
from knack.util import CLIError
from knack.log import get_logger
from azext_iot.constants import CENTRAL_ENDPOINT
from azext_iot.central import services as central_services
from azext_iot.central.models.enum import ApiVersion
from azext_iot.central import models as central_models

logger = get_logger(__name__)


class CentralRoleProviderPreview:
    def __init__(self, cmd, app_id: str, token=None):
        """
        Provider for roles APIs

        Args:
            cmd: command passed into az
            app_id: name of app (used for forming request URL)
            token: (OPTIONAL) authorization token to fetch device details from IoTC.
                MUST INCLUDE type (e.g. 'SharedAccessToken ...', 'Bearer ...')
                Useful in scenarios where user doesn't own the app
                therefore AAD token won't work, but a SAS token generated by owner will
        """
        self._cmd = cmd
        self._app_id = app_id
        self._token = token
        self._roles = {}

    def list_roles(self, central_dns_suffix=CENTRAL_ENDPOINT) -> List[RolePreview]:
        roles = central_services.role.list_roles(
            cmd=self._cmd,
            app_id=self._app_id,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=ApiVersion.preview.value,
        )

        # add to cache
        self._roles.update({role.id: role for role in roles})

        return self._roles

    def get_role(
        self, role_id, central_dns_suffix=CENTRAL_ENDPOINT,
    ) -> central_models.RolePreview:
        # get or add to cache
        role = self._roles.get(role_id)
        if not role:
            role = central_services.role.get_role(
                cmd=self._cmd,
                app_id=self._app_id,
                role_id=role_id,
                token=self._token,
                central_dns_suffix=central_dns_suffix,
                api_version=ApiVersion.preview.value,
            )
            self._roles[role_id] = role

        if not role:
            raise CLIError("No role found with id: '{}'.".format(role_id))

        return role