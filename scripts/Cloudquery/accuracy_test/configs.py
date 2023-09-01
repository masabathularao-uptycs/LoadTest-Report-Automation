from pathlib import Path

json_directory = "expected_logs"
PROJECT_ROOT = Path(__file__).resolve().parent
# Initialize a dictionary to store the total counts
total_counts = {"aws_cloudtrail_events": {"added": 0}, "aws_ec2_instance": {"added": 0, "removed": 0, "modified": 0}, "aws_ec2_address": {"added": 0, "removed": 0, "modified": 0}, "aws_ec2_image": {"added": 0, "removed": 0, "modified": 0}, "aws_ec2_snapshot": {"added": 0, "removed": 0, "modified": 0}, "aws_ec2_volume": {"added": 0, "removed": 0, "modified": 0}, "aws_ecr_repository": {"added": 0, "removed": 0, "modified": 0}, "aws_ecs_cluster": {"added": 0, "removed": 0, "modified": 0}, "aws_iam_group": {"added": 0, "removed": 0, "modified": 0}, "aws_iam_policy": {"added": 0, "removed": 0, "modified": 0}, "aws_iam_role": {"added": 0, "removed": 0, "modified": 0}, "aws_iam_user": {"added": 0, "removed": 0}, "aws_organizations_account": {"added": 0, "removed": 0}, "aws_elasticache_replication_group": {"added": 0, "removed": 0, "modified": 0}, "aws_elasticache_cluster": {"added": 0, "removed": 0, "modified": 0}, "aws_efs_file_system": {"added": 0, "removed": 0, "modified": 0}, "aws_codepipeline": {"added": 0, "removed": 0}, "aws_codedeploy_application": {"added": 0, "removed": 0}, "aws_servicecatalog_portfolio": {"added": 0, "removed": 0}, "aws_config_delivery_channel": {"added": 0, "removed": 0}, "aws_guardduty_detector": {"added": 0, "removed": 0}, "aws_directoryservice_directory": {"added": 0, "removed": 0}, "aws_wafv2_web_acl": {"added": 0, "removed": 0}, "aws_securityhub_hub": {"added": 0, "removed": 0}, "aws_workspaces_workspace": {"added": 0, "removed": 0}, "aws_ec2_subnet": {"added": 0, "removed": 0, "modified": 0}, "aws_redshift_cluster": {"added": 0, "removed": 0, "modified": 0}, "aws_s3_bucket": {"added": 0, "removed": 0, "modified": 0}, "aws_rds_db_instance": {"added": 0, "removed": 0, "modified": 0}, "aws_rds_db_cluster": {"added": 0, "removed": 0, "modified": 0}, "aws_rds_db_snapshot": {"added": 0, "removed": 0, "modified": 0}, "aws_cloudtrail_trail": {"added": 0, "removed": 0, "modified": 0}, "aws_eks_cluster": {"added": 0, "removed": 0, "modified": 0}, "aws_ec2_vpc": {"added": 0, "removed": 0, "modified": 0}, "aws_ec2_security_group": {"added": 0, "removed": 0, "modified": 0}, "aws_ec2_network_acl": {"added": 0, "removed": 0, "modified": 0}, "aws_elb": {"added": 0, "removed": 0, "modified": 0}, "aws_glacier_vault": {"added": 0, "removed": 0, "modified": 0}, "aws_lambda_function": {"added": 0, "removed": 0, "modified": 0}, "aws_sqs_queue": {"added": 0, "removed": 0, "modified": 0}, "aws_sns_topic": {"added": 0, "removed": 0, "modified": 0}, "aws_cloudfront_distribution": {"added": 0, "removed": 0, "modified": 0}, "aws_codecommit_repository": {"added": 0, "removed": 0, "modified": 0}, "aws_kinesis_data_stream": {"added": 0, "removed": 0, "modified": 0}, "aws_api_gateway_rest_api": {"added": 0, "removed": 0, "modified": 0}, "aws_route53_domain": {"added": 0, "removed": 0, "modified": 0}, "aws_route53_hosted_zone": {"added": 0, "removed": 0, "modified": 0}, "aws_cloudwatch_metric_alarm": {"added": 0, "removed": 0, "modified": 0}, "aws_cloudformation_stack": {"added": 0, "removed": 0, "modified": 0}, "aws_ssm_managed_instance": {"added": 0, "removed": 0, "modified": 0}, "aws_ram_resource_share": {"added": 0, "removed": 0, "modified": 0}, "aws_secretsmanager_secret": {"added": 0, "removed": 0, "modified": 0}, "aws_kms_key": {"added": 0, "removed": 0, "modified": 0}}
#total_counts={"gcp_cloud_log_events":{"added":0},"gcp_secret_manager_secret":{"added":0,"removed":0,"modified":0},"gcp_secret_manager_secret_version":{"added":0,"removed":0,"modified":0},"gcp_kms_key":{"added":0,"removed":0,"modified":0},"gcp_cloud_run_revision":{"added":0,"removed":0,"modified":0},"gcp_cloud_run_service":{"added":0,"removed":0,"modified":0},"gcp_cloud_function":{"added":0,"removed":0,"modified":0},"gcp_memorystore_memcached_instance":{"added":0,"removed":0,"modified":0},"gcp_memorystore_redis_instance":{"added":0,"removed":0,"modified":0},"gcp_bigquery_dataset":{"added":0,"removed":0,"modified":0},"gcp_bigquery_table":{"added":0,"removed":0,"modified":0},"gcp_sql_instance":{"added":0,"removed":0,"modified":0},"gcp_sql_database":{"added":0,"removed":0,"modified":0},"gcp_iam_service_account":{"added":0,"removed":0,"modified":0},"gcp_iam_role":{"added":0,"removed":0,"modified":0},"gcp_pubsub_subscription":{"added":0,"removed":0},"gcp_pubsub_topic":{"added":0,"removed":0,"modified":0},"gcp_dns_managed_zone":{"added":0,"removed":0,"modified":0},"gcp_dns_policy":{"added":0,"removed":0,"modified":0},"gcp_monitoring_alert_policy":{"added":0,"removed":0,"modified":0},"gcp_logging_sink":{"added":0,"removed":0,"modified":0},"gcp_logging_metric":{"added":0,"removed":0,"modified":0},"gcp_file_instance":{"added":0,"removed":0},"gcp_file_backup":{"added":0,"removed":0},"gcp_storage_bucket":{"added":0,"removed":0,"modified":0},"gcp_container_cluster":{"added":0,"removed":0},"gcp_compute_instance":{"added":0,"removed":0,"modified":0},"gcp_compute_image":{"added":0,"modified":0},"gcp_compute_disk":{"added":0,"removed":0,"modified":0}}


domain='mercury'
#api_path = str(PROJECT_ROOT)  + '/api_keys/{}_api.json'.format(domain)
api_path = str(PROJECT_ROOT)  + '/api_keys/{}_multicustomer_api.json'.format(domain)


query_api='https://{}{}/public/api/customers/{}/queryJobs'
payload={"query":"select upt_added,count(*) from {} where upt_day >= 2022-07-13 and upt_time >= timestamp '{}' and upt_time < timestamp '{}' group by upt_added;","type":"global","filters":{},"parameters":[],"parameterValues":{},"agentType":"asset"}
result_api='https://{}{}/public/api/customers/{}/queryJobs/{}/results?limit=10000'

#
load_start='2023-08-23 19:03:15'
load_end='2023-08-24 07:03:42'