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
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.monitor_threshold import MonitorThreshold
from ri.apiclient.models.rime_long_description_tab import RimeLongDescriptionTab
from ri.apiclient.models.rime_monitor_data_point import RimeMonitorDataPoint
from ri.apiclient.models.rime_uuid import RimeUUID
from typing import Optional, Set
from typing_extensions import Self

class RimeGetMonitorResultResponse(BaseModel):
    """
    GetMonitorResultResponse returns the results for a monitor within a time range.
    """ # noqa: E501
    monitor_id: Optional[RimeUUID] = Field(default=None, alias="monitorId")
    monitor_name: Optional[StrictStr] = Field(default=None, description="The name of the monitor.", alias="monitorName")
    metric_name: Optional[StrictStr] = Field(default=None, alias="metricName")
    threshold: Optional[MonitorThreshold] = None
    data_points: Optional[List[RimeMonitorDataPoint]] = Field(default=None, description="The monitor data points.", alias="dataPoints")
    description_html: Optional[StrictStr] = Field(default=None, description="Description of the monitor that may contain HTML.", alias="descriptionHtml")
    long_description_tabs: Optional[List[RimeLongDescriptionTab]] = Field(default=None, description="More detailed information about the monitor.", alias="longDescriptionTabs")
    __properties: ClassVar[List[str]] = ["monitorId", "monitorName", "metricName", "threshold", "dataPoints", "descriptionHtml", "longDescriptionTabs"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RimeGetMonitorResultResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of monitor_id
        if self.monitor_id:
            _dict['monitorId'] = self.monitor_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of threshold
        if self.threshold:
            _dict['threshold'] = self.threshold.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in data_points (list)
        _items = []
        if self.data_points:
            for _item in self.data_points:
                if _item:
                    _items.append(_item.to_dict())
            _dict['dataPoints'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in long_description_tabs (list)
        _items = []
        if self.long_description_tabs:
            for _item in self.long_description_tabs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['longDescriptionTabs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RimeGetMonitorResultResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "monitorId": RimeUUID.from_dict(obj["monitorId"]) if obj.get("monitorId") is not None else None,
            "monitorName": obj.get("monitorName"),
            "metricName": obj.get("metricName"),
            "threshold": MonitorThreshold.from_dict(obj["threshold"]) if obj.get("threshold") is not None else None,
            "dataPoints": [RimeMonitorDataPoint.from_dict(_item) for _item in obj["dataPoints"]] if obj.get("dataPoints") is not None else None,
            "descriptionHtml": obj.get("descriptionHtml"),
            "longDescriptionTabs": [RimeLongDescriptionTab.from_dict(_item) for _item in obj["longDescriptionTabs"]] if obj.get("longDescriptionTabs") is not None else None
        })
        return _obj


