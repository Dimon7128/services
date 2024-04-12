import json
import boto3
import os

def lambda_handler(event, context):
    route53 = boto3.client('route53')
    dns_name = event['alb_dns_name']
    hosted_zone_id = 'Z05048322XLKJHO3HU4'  # The ID 
    alb_zone_id = os.environ['DB_NAME']  # Replace with the actual ALB hosted zone ID for your region

    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'dimaubapp.cloud',  # Replace with your actual domain
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': alb_zone_id,
                            'DNSName': dns_name,
                            'EvaluateTargetHealth': False
                        }
                    }
                }
            ]
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('DNS Update Successful')
    }
