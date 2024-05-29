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

from ri.apiclient.models.list_agents_request_list_agents_query import ListAgentsRequestListAgentsQuery

class TestListAgentsRequestListAgentsQuery(unittest.TestCase):
    """ListAgentsRequestListAgentsQuery unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ListAgentsRequestListAgentsQuery:
        """Test ListAgentsRequestListAgentsQuery
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ListAgentsRequestListAgentsQuery`
        """
        model = ListAgentsRequestListAgentsQuery()
        if include_optional:
            return ListAgentsRequestListAgentsQuery(
                agent_status_types = [
                    'AGENT_STATUS_UNSPECIFIED'
                    ],
                agent_ids = [
                    ''
                    ],
                type = 'AGENT_TYPE_VALIDATION'
            )
        else:
            return ListAgentsRequestListAgentsQuery(
        )
        """

    def testListAgentsRequestListAgentsQuery(self):
        """Test ListAgentsRequestListAgentsQuery"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()