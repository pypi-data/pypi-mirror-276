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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from ri.apiclient.models.custom_metric_custom_metric_metadata import CustomMetricCustomMetricMetadata
from typing import Optional, Set
from typing_extensions import Self

class TestrunCustomMetric(BaseModel):
    """
    Specifies configuration values for a custom metric.
    """ # noqa: E501
    name: StrictStr = Field(description="Name of the custom metric.")
    file_path: StrictStr = Field(description="Path to the file with metric definition.", alias="filePath")
    range_lower_bound: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Valid range lower bound.", alias="rangeLowerBound")
    range_upper_bound: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Valid range upper bound.", alias="rangeUpperBound")
    run_subset_performance: Optional[StrictBool] = Field(default=None, description="Should run subset performance.", alias="runSubsetPerformance")
    run_subset_performance_drift: Optional[StrictBool] = Field(default=None, description="Should run subset performance drift.", alias="runSubsetPerformanceDrift")
    run_overall_performance: Optional[StrictBool] = Field(default=None, description="Should run overall performance.", alias="runOverallPerformance")
    metadata: Optional[CustomMetricCustomMetricMetadata] = None
    __properties: ClassVar[List[str]] = ["name", "filePath", "rangeLowerBound", "rangeUpperBound", "runSubsetPerformance", "runSubsetPerformanceDrift", "runOverallPerformance", "metadata"]

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
        """Create an instance of TestrunCustomMetric from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestrunCustomMetric from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "filePath": obj.get("filePath"),
            "rangeLowerBound": obj.get("rangeLowerBound"),
            "rangeUpperBound": obj.get("rangeUpperBound"),
            "runSubsetPerformance": obj.get("runSubsetPerformance"),
            "runSubsetPerformanceDrift": obj.get("runSubsetPerformanceDrift"),
            "runOverallPerformance": obj.get("runOverallPerformance"),
            "metadata": CustomMetricCustomMetricMetadata.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None
        })
        return _obj


