# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021-2024 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************
import logging

from .api_key.comet_api_key import parse_api_key
from .connection_helpers import get_root_url
from .logging_messages import BASE_URL_MISMATCH_CONFIG_API_KEY
from .settings import MPMSettings

LOGGER = logging.getLogger(__name__)

DEFAULT_COMET_BASE_URL = "https://www.comet.com/"


def extract_comet_url(settings: MPMSettings) -> str:
    api_key = parse_api_key(settings.api_key)
    if api_key is None:
        return DEFAULT_COMET_BASE_URL

    if settings.url is not None and settings.url != "":
        settings_base_url = get_root_url(settings.url)
        if api_key.base_url is not None and api_key.base_url != settings_base_url:
            LOGGER.warning(
                BASE_URL_MISMATCH_CONFIG_API_KEY, settings_base_url, api_key.base_url
            )
        # do not change base url
        return settings.url

    if api_key.base_url is not None:
        return api_key.base_url

    return DEFAULT_COMET_BASE_URL
