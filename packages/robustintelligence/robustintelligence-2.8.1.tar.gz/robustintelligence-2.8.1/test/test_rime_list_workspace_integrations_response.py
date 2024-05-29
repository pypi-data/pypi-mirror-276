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

from ri.apiclient.models.rime_list_workspace_integrations_response import RimeListWorkspaceIntegrationsResponse

class TestRimeListWorkspaceIntegrationsResponse(unittest.TestCase):
    """RimeListWorkspaceIntegrationsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RimeListWorkspaceIntegrationsResponse:
        """Test RimeListWorkspaceIntegrationsResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RimeListWorkspaceIntegrationsResponse`
        """
        model = RimeListWorkspaceIntegrationsResponse()
        if include_optional:
            return RimeListWorkspaceIntegrationsResponse(
                integration_infos = [
                    ri.apiclient.models.rime_integration_info.rimeIntegrationInfo(
                        integration = ri.apiclient.models.rischemaintegration_integration.rischemaintegrationIntegration(
                            id = ri.apiclient.models.rime_uuid.rimeUUID(
                                uuid = '', ), 
                            workspace_id = ri.apiclient.models.rime_uuid.rimeUUID(
                                uuid = '', ), 
                            creation_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            name = '', 
                            type = 'INTEGRATION_TYPE_UNSPECIFIED', 
                            schema = ri.apiclient.models.integration_integration_schema.integrationIntegrationSchema(
                                variables = [
                                    ri.apiclient.models.for_further_information_on_supported_integration_variables,_visit
https://docs/robustintelligence/com/en/latest/administration/workspace_configuration/integrations/configuring_integrations/html.For further information on supported integration variables, visit
https://docs.robustintelligence.com/en/latest/administration/workspace_configuration/integrations/configuring_integrations.html(
                                        name = '', 
                                        sensitivity = 'VARIABLE_SENSITIVITY_UNSPECIFIED', 
                                        value = '', )
                                    ], ), 
                            level = 'INTEGRATION_LEVEL_UNSPECIFIED', ), 
                        configured = True, )
                    ]
            )
        else:
            return RimeListWorkspaceIntegrationsResponse(
        )
        """

    def testRimeListWorkspaceIntegrationsResponse(self):
        """Test RimeListWorkspaceIntegrationsResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()