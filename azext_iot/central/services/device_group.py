# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# This is largely derived from https://docs.microsoft.com/en-us/rest/api/iotcentral/deviceGroups

from typing import List
import requests

from knack.util import CLIError
from knack.log import get_logger

from azext_iot.constants import CENTRAL_ENDPOINT
from azext_iot.central.services import _utility
from azext_iot.central import models as central_models
from azext_iot.central.models.enum import ApiVersion

logger = get_logger(__name__)

BASE_PATH = "api/deviceGroups"


def list_device_groups(
    cmd,
    app_id: str,
    token: str,
    max_pages=1,
    central_dns_suffix=CENTRAL_ENDPOINT,
    api_version=ApiVersion.preview.value,
) -> List[central_models.DeviceGroupPreview]:
    """
    Get a list of all device groups in IoTC app

    Args:
        cmd: command passed into az
        app_id: name of app (used for forming request URL)
        token: (OPTIONAL) authorization token to fetch device details from IoTC.
            MUST INCLUDE type (e.g. 'SharedAccessToken ...', 'Bearer ...')
        central_dns_suffix: {centralDnsSuffixInPath} as found in docs

    Returns:
        list of device groups
    """

    device_groups = []

    url = "https://{}.{}/{}".format(app_id, central_dns_suffix, BASE_PATH)
    headers = _utility.get_headers(token, cmd)

    # Construct parameters
    query_parameters = {}
    query_parameters["api-version"] = api_version

    pages_processed = 0
    while (pages_processed <= max_pages) and url:
        response = requests.get(url, headers=headers, params=query_parameters)
        result = _utility.try_extract_result(response)

        if "value" not in result:
            raise CLIError("Value is not present in body: {}".format(result))

        device_groups = device_groups + [
            central_models.DeviceGroupPreview(device_group) for device_group in result["value"]
        ]

        try:
            url = result.get("nextLink", params=query_parameters)
        except:
            pass
        pages_processed = pages_processed + 1

    return device_groups