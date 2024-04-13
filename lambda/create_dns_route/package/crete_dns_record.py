import json
import boto3
import os

def lambda_handler(event, context):
    route53 = boto3.client('route53')

    # Use get to avoid KeyError if 'alb_dns_name' is not in the event
    dns_name = os.environ.get('ALB_DNS_NAME')
    if dns_name is None:
        return {
            'statusCode': 400,
            'body': json.dumps("The event does not contain 'alb_dns_name'")
        }

    hosted_zone_id = 'Z05408322IXL3KHJO3HU4'  # The ID
    alb_zone_id = os.environ.get('ALB_ZONE_ID')  # Ensure this environment variable is set correctly

    if alb_zone_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps("ALB_ZONpip install -r requirements.txt -t ./packageE_ID environment variable is not set")
        }

    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'dimabuapp.cloud',  # Replace with your actual domain
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
