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
from ri.apiclient.models.runtimeinfo_run_time_info import RuntimeinfoRunTimeInfo
from typing import Optional, Set
from typing_extensions import Self

class TestrunTestRunIncrementalConfig(BaseModel):
    """
    TestRunIncrementalConfig contains the configuration necessary to run a Continuous Test.
    """ # noqa: E501
    eval_dataset_id: Optional[StrictStr] = Field(default=None, description="Uniquely specifies an evaluation Dataset.", alias="evalDatasetId")
    run_time_info: Optional[RuntimeinfoRunTimeInfo] = Field(default=None, alias="runTimeInfo")
    __properties: ClassVar[List[str]] = ["evalDatasetId", "runTimeInfo"]

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
        """Create an instance of TestrunTestRunIncrementalConfig from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of run_time_info
        if self.run_time_info:
            _dict['runTimeInfo'] = self.run_time_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestrunTestRunIncrementalConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "evalDatasetId": obj.get("evalDatasetId"),
            "runTimeInfo": RuntimeinfoRunTimeInfo.from_dict(obj["runTimeInfo"]) if obj.get("runTimeInfo") is not None else None
        })
        return _obj


