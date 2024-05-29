# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import unittest

from ri.apiclient.models.generativefirewall_language_detection_rule_config import GenerativefirewallLanguageDetectionRuleConfig

class TestGenerativefirewallLanguageDetectionRuleConfig(unittest.TestCase):
    """GenerativefirewallLanguageDetectionRuleConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GenerativefirewallLanguageDetectionRuleConfig:
        """Test GenerativefirewallLanguageDetectionRuleConfig
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GenerativefirewallLanguageDetectionRuleConfig`
        """
        model = GenerativefirewallLanguageDetectionRuleConfig()
        if include_optional:
            return GenerativefirewallLanguageDetectionRuleConfig(
                whitelisted_languages = [
                    'LANGUAGE_UNSPECIFIED'
                    ]
            )
        else:
            return GenerativefirewallLanguageDetectionRuleConfig(
        )
        """

    def testGenerativefirewallLanguageDetectionRuleConfig(self):
        """Test GenerativefirewallLanguageDetectionRuleConfig"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()