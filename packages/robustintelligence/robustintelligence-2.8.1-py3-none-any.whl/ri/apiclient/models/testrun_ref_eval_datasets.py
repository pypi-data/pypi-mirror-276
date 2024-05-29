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
from ri.apiclient.models.rime_time_interval import RimeTimeInterval
from typing import Optional, Set
from typing_extensions import Self

class TestrunRefEvalDatasets(BaseModel):
    """
    RefEvalDatasets uniquely specifies information about reference and evaluation Datasets.
    """ # noqa: E501
    ref_dataset_id: Optional[StrictStr] = Field(default=None, description="Uniquely specifies a reference Dataset.", alias="refDatasetId")
    eval_dataset_id: StrictStr = Field(description="Uniquely specifies an evaluation Dataset.", alias="evalDatasetId")
    eval_dataset_time_interval: Optional[RimeTimeInterval] = Field(default=None, alias="evalDatasetTimeInterval")
    __properties: ClassVar[List[str]] = ["refDatasetId", "evalDatasetId", "evalDatasetTimeInterval"]

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
        """Create an instance of TestrunRefEvalDatasets from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of eval_dataset_time_interval
        if self.eval_dataset_time_interval:
            _dict['evalDatasetTimeInterval'] = self.eval_dataset_time_interval.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestrunRefEvalDatasets from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "refDatasetId": obj.get("refDatasetId"),
            "evalDatasetId": obj.get("evalDatasetId"),
            "evalDatasetTimeInterval": RimeTimeInterval.from_dict(obj["evalDatasetTimeInterval"]) if obj.get("evalDatasetTimeInterval") is not None else None
        })
        return _obj


