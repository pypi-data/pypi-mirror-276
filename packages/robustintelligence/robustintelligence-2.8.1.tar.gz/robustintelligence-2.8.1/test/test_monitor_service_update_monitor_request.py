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

from ri.apiclient.models.monitor_service_update_monitor_request import MonitorServiceUpdateMonitorRequest

class TestMonitorServiceUpdateMonitorRequest(unittest.TestCase):
    """MonitorServiceUpdateMonitorRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MonitorServiceUpdateMonitorRequest:
        """Test MonitorServiceUpdateMonitorRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MonitorServiceUpdateMonitorRequest`
        """
        model = MonitorServiceUpdateMonitorRequest()
        if include_optional:
            return MonitorServiceUpdateMonitorRequest(
                monitor = ri.apiclient.models.monitor_service_update_monitor_request_monitor.MonitorService_UpdateMonitor_request_monitor(
                    id = ri.apiclient.models.uniquely_specifies_a_monitor/.Uniquely specifies a Monitor.(), 
                    name = '', 
                    firewall_id = ri.apiclient.models.rime_uuid.rimeUUID(
                        uuid = '', ), 
                    monitor_type = 'MONITOR_TYPE_UNSPECIFIED', 
                    risk_category_type = 'RISK_CATEGORY_TYPE_UNSPECIFIED', 
                    test_category = 'TEST_CATEGORY_TYPE_UNSPECIFIED', 
                    artifact_identifier = ri.apiclient.models.monitor_artifact_identifier.monitorArtifactIdentifier(
                        test_case_metric_identifier = ri.apiclient.models.artifact_identifier_test_case_metric_identifier.ArtifactIdentifierTestCaseMetricIdentifier(
                            test_batch_id = '', 
                            metric = '', 
                            feature_names = [
                                ''
                                ], ), 
                        category_test_metric_identifier = ri.apiclient.models.artifact_identifier_category_test_identifier.ArtifactIdentifierCategoryTestIdentifier(
                            metric = '', ), 
                        subset_test_metric_identifier = ri.apiclient.models.in_order_to_specify_a_test_case_metric_identifier,_test_batch_type,_feature_name
and_metric_are_required/_note_that_each_of_them_refer_to_fields_in_the
test_case_doc/_metric_refers_to_a_single_metric_in_array_test_metric
(in_the_test_case_doc)/
for_example_for_some_test_case_doc:
{
___///
___test_batch_type:_'subset_performance:subset_positive_prediction_rate',
___feature_id:_'xxxx',
___metrics:_[
_____{
_______category:_14,
_______metric:_'worst_perf_diff',
_______data:_{float_value:_0/032836160521054425},
_______data_type:_1
_____},
_____{
_____category:_14,
_________metric:_'names',
_________data:_{_str_list:_[_'credit',_'debit',_'null'_]_},
_________data_type:_1
_____},
___]
}
we_can_specify_test_case_metric_identifier_as:
{
___test_batch_id_=_'subset_performance:subset_positive_prediction_rate',
___feature_id_=_'xxxx',
___metric_=_'names',
}.In order to specify a TestCaseMetricIdentifier, TestBatchType, FeatureName
and Metric are required. Note that each of them refer to fields in the
TestCase doc. Metric refers to a single Metric in array TestMetric
(in the TestCase doc).
For example for some TestCase Doc:
{
   ...
   test_batch_type: 'subset_performance:subset_positive_prediction_rate',
   feature_id: 'xxxx',
   metrics: [
     {
       category: 14,
       metric: 'worst_perf_diff',
       data: {float_value: 0.032836160521054425},
       data_type: 1
     },
     {
     category: 14,
         metric: 'names',
         data: { str_list: [ 'credit', 'debit', 'null' ] },
         data_type: 1
     },
   ]
}
We can specify TestCaseMetricIdentifier as:
{
   test_batch_id = 'subset_performance:subset_positive_prediction_rate',
   feature_id = 'xxxx',
   metric = 'names',
}(
                            test_batch_id = '', 
                            metric = '', 
                            subset_name = '', ), ), 
                    created_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    notify = True, 
                    config = ri.apiclient.models.schemamonitor_config.schemamonitorConfig(
                        degradation = ri.apiclient.models.monitor_metric_degradation_config.monitorMetricDegradationConfig(
                            aggregation = ri.apiclient.models.defines_an_aggregation_for_a_metric
aggregations_take_in_a_time_series_and_output_a_time_series.Defines an aggregation for a metric
Aggregations take in a time series and output a time series(
                                aggregation_type = 'AGGREGATION_TYPE_UNSPECIFIED', 
                                time_window = '', ), 
                            transform = ri.apiclient.models.defines_a_transformation_function_for_the_metric
transformations_take_in_a_time_series_and_output_a_time_series.Defines a transformation function for the metric
Transformations take in a time series and output a time series(
                                difference_from_target = ri.apiclient.models.monitor_difference_from_target.monitorDifferenceFromTarget(
                                    difference = 'DIFFERENCE_UNSPECIFIED', 
                                    target = 'TARGET_UNSPECIFIED', ), ), 
                            threshold = ri.apiclient.models.thresholds_defined_for_the_monitor.Thresholds defined for the Monitor(
                                low = 1.337, 
                                high = 1.337, 
                                type = 'TYPE_UNSPECIFIED', ), ), 
                        anomaly = ri.apiclient.models.monitor_anomaly_config.monitorAnomalyConfig(), ), 
                    excluded_transforms = ri.apiclient.models.monitor_excluded_transforms.monitorExcludedTransforms(), 
                    pinned = True, ),
                mask = ''
            )
        else:
            return MonitorServiceUpdateMonitorRequest(
        )
        """

    def testMonitorServiceUpdateMonitorRequest(self):
        """Test MonitorServiceUpdateMonitorRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()