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

from ri.apiclient.models.testrunresult_result_summary_counts import TestrunresultResultSummaryCounts

class TestTestrunresultResultSummaryCounts(unittest.TestCase):
    """TestrunresultResultSummaryCounts unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TestrunresultResultSummaryCounts:
        """Test TestrunresultResultSummaryCounts
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TestrunresultResultSummaryCounts`
        """
        model = TestrunresultResultSummaryCounts()
        if include_optional:
            return TestrunresultResultSummaryCounts(
                total = '',
                var_pass = '',
                warning = '',
                fail = '',
                skip = ''
            )
        else:
            return TestrunresultResultSummaryCounts(
        )
        """

    def testTestrunresultResultSummaryCounts(self):
        """Test TestrunresultResultSummaryCounts"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()