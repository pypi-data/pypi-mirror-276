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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.monitor_artifact_identifier import MonitorArtifactIdentifier
from ri.apiclient.models.monitor_excluded_transforms import MonitorExcludedTransforms
from ri.apiclient.models.monitor_monitor_type import MonitorMonitorType
from ri.apiclient.models.rime_uuid import RimeUUID
from ri.apiclient.models.riskscore_risk_category_type import RiskscoreRiskCategoryType
from ri.apiclient.models.schemamonitor_config import SchemamonitorConfig
from ri.apiclient.models.testrun_test_category_type import TestrunTestCategoryType
from typing import Optional, Set
from typing_extensions import Self

class MonitorMonitor(BaseModel):
    """
    MonitorMonitor
    """ # noqa: E501
    id: RimeUUID
    name: Optional[StrictStr] = Field(default=None, description="The name of the monitor.")
    firewall_id: Optional[RimeUUID] = Field(default=None, alias="firewallId")
    monitor_type: Optional[MonitorMonitorType] = Field(default=None, alias="monitorType")
    risk_category_type: Optional[RiskscoreRiskCategoryType] = Field(default=None, alias="riskCategoryType")
    test_category: Optional[TestrunTestCategoryType] = Field(default=None, alias="testCategory")
    artifact_identifier: Optional[MonitorArtifactIdentifier] = Field(default=None, alias="artifactIdentifier")
    created_time: Optional[datetime] = Field(default=None, description="The time at which the monitor was created.", alias="createdTime")
    notify: Optional[StrictBool] = Field(default=None, description="This field indicates whether the system should send CT monitoring notifications when this monitor is triggered. For default monitors, after the RIME engine creates a Monitor, this field should only be modified directly by the user. i.e. when we upsert the monitor in the Result synthesizer, we must not overwrite the value configured by the user.")
    config: Optional[SchemamonitorConfig] = None
    excluded_transforms: Optional[MonitorExcludedTransforms] = Field(default=None, alias="excludedTransforms")
    pinned: Optional[StrictBool] = Field(default=None, description="Option to pin a monitor. Pinned monitors are pinned for all users visiting the monitor's project.")
    __properties: ClassVar[List[str]] = ["id", "name", "firewallId", "monitorType", "riskCategoryType", "testCategory", "artifactIdentifier", "createdTime", "notify", "config", "excludedTransforms", "pinned"]

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
        """Create an instance of MonitorMonitor from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of id
        if self.id:
            _dict['id'] = self.id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of firewall_id
        if self.firewall_id:
            _dict['firewallId'] = self.firewall_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of artifact_identifier
        if self.artifact_identifier:
            _dict['artifactIdentifier'] = self.artifact_identifier.to_dict()
        # override the default output from pydantic by calling `to_dict()` of config
        if self.config:
            _dict['config'] = self.config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of excluded_transforms
        if self.excluded_transforms:
            _dict['excludedTransforms'] = self.excluded_transforms.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MonitorMonitor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": RimeUUID.from_dict(obj["id"]) if obj.get("id") is not None else None,
            "name": obj.get("name"),
            "firewallId": RimeUUID.from_dict(obj["firewallId"]) if obj.get("firewallId") is not None else None,
            "monitorType": obj.get("monitorType"),
            "riskCategoryType": obj.get("riskCategoryType"),
            "testCategory": obj.get("testCategory"),
            "artifactIdentifier": MonitorArtifactIdentifier.from_dict(obj["artifactIdentifier"]) if obj.get("artifactIdentifier") is not None else None,
            "createdTime": obj.get("createdTime"),
            "notify": obj.get("notify"),
            "config": SchemamonitorConfig.from_dict(obj["config"]) if obj.get("config") is not None else None,
            "excludedTransforms": MonitorExcludedTransforms.from_dict(obj["excludedTransforms"]) if obj.get("excludedTransforms") is not None else None,
            "pinned": obj.get("pinned")
        })
        return _obj


