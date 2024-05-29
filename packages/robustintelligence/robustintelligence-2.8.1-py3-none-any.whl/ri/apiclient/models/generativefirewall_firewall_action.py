# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class GenerativefirewallFirewallAction(str, Enum):
    """
    FirewallAction is the action the firewall takes on model input or output. This serves as a recommendation to the client's system whether to accept the input / output pair or reject it.
    """

    """
    allowed enum values
    """
    FIREWALL_ACTION_UNSPECIFIED = 'FIREWALL_ACTION_UNSPECIFIED'
    FIREWALL_ACTION_ALLOW = 'FIREWALL_ACTION_ALLOW'
    FIREWALL_ACTION_FLAG = 'FIREWALL_ACTION_FLAG'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of GenerativefirewallFirewallAction from a JSON string"""
        return cls(json.loads(json_str))


