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


class MonitorAggregationType(str, Enum):
    """
    MonitorAggregationType
    """

    """
    allowed enum values
    """
    AGGREGATION_TYPE_AVG = 'AGGREGATION_TYPE_AVG'
    AGGREGATION_TYPE_MIN = 'AGGREGATION_TYPE_MIN'
    AGGREGATION_TYPE_MAX = 'AGGREGATION_TYPE_MAX'
    AGGREGATION_TYPE_SUM = 'AGGREGATION_TYPE_SUM'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of MonitorAggregationType from a JSON string"""
        return cls(json.loads(json_str))


