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

from ri.apiclient.models.project_service_update_user_of_project_request import ProjectServiceUpdateUserOfProjectRequest

class TestProjectServiceUpdateUserOfProjectRequest(unittest.TestCase):
    """ProjectServiceUpdateUserOfProjectRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProjectServiceUpdateUserOfProjectRequest:
        """Test ProjectServiceUpdateUserOfProjectRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProjectServiceUpdateUserOfProjectRequest`
        """
        model = ProjectServiceUpdateUserOfProjectRequest()
        if include_optional:
            return ProjectServiceUpdateUserOfProjectRequest(
                project_id = ri.apiclient.models.uniquely_specifies_a_project/.Uniquely specifies a Project.(),
                user = ri.apiclient.models.project_service_update_user_of_project_request_user.ProjectService_UpdateUserOfProject_request_user(
                    user_id = ri.apiclient.models.user_id.userId(), 
                    user_role = 'ACTOR_ROLE_UNSPECIFIED', )
            )
        else:
            return ProjectServiceUpdateUserOfProjectRequest(
        )
        """

    def testProjectServiceUpdateUserOfProjectRequest(self):
        """Test ProjectServiceUpdateUserOfProjectRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()