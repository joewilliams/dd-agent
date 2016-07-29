# stdlib
from types import ListType

# 3p
from nose.plugins.attrib import attr

# project
from tests.checks.common import AgentCheckTest


"""
Run the following on your local SQL Server:

CREATE LOGIN datadog WITH PASSWORD = '340$Uuxwp7Mcxo7Khy';
CREATE USER datadog FOR LOGIN datadog;
GRANT SELECT on sys.dm_os_performance_counters to datadog;
GRANT VIEW SERVER STATE to datadog;
"""

CONFIG = {
    'init_config': {
        'custom_metrics': [
            {
                'name': 'sqlserver.clr.execution',
                'type': 'gauge',
                'counter_name': 'CLR Execution',
            },
            {
                'name': 'sqlserver.exec.in_progress',
                'type': 'gauge',
                'counter_name': 'OLEDB calls',
                'instance_name': 'Cumulative execution time (ms) per second',
            },
            {
                'name': 'sqlserver.db.commit_table_entries',
                'type': 'gauge',
                'counter_name': 'Log Flushes/sec',
                'instance_name': 'ALL',
                'tag_by': 'db',
            },
        ],
    },
    'instances': [
        {
            'host': '127.0.0.1,1433',
            'username': 'sa',
            'password': 'Password12!',
        },
    ],
}


@attr('windows')
@attr(requires='windows')
class SQLServerTest(AgentCheckTest):
    CHECK_NAME = 'sqlserver'

    def testSqlServer(self):
        self.run_check(CONFIG)

        # Make sure the base metrics loaded
        # base_metrics = [m[0] for m in check.METRICS]
        # ret_metrics = [m[0] for m in metrics]
        # for metric in base_metrics:
        #     assert metric in ret_metrics

        # Check our custom metrics
        self.assertMetric('sqlserver.clr.execution', at_least=1)
        self.assertMetric('sqlserver.exec.in_progress', at_least=1)
        self.assertMetric('sqlserver.db.commit_table_entries', at_least=1)

        # # Make sure the ALL custom metric is tagged
        # tagged_metrics = [m for m in metrics
        #     if m[0] == 'sqlserver.db.commit_table_entries']
        # for metric in tagged_metrics:
        #     for tag in metric[3]['tags']:
        #         assert tag.startswith('db')

        # # Service checks
        # service_checks = check.get_service_checks()
        # service_checks_count = len(service_checks)
        # self.assertTrue(isinstance(metrics, ListType))
        # self.assertTrue(service_checks_count > 0)
        # self.assertEquals(len([sc for sc in service_checks if sc['check'] == check.SERVICE_CHECK_NAME]), 1, service_checks)
        # # Assert that all service checks have the proper tags: host and port
        # self.assertEquals(len([sc for sc in service_checks if "host:127.0.0.1,1433" in sc['tags']]), service_checks_count, service_checks)
        # self.assertEquals(len([sc for sc in service_checks if "db:master" in sc['tags']]), service_checks_count, service_checks)
