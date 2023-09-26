import boto3
import datetime
import pytz

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2 = boto3.client('ec2')
    cloudwatch = boto3.client('cloudwatch')

    # Convert current UTC time to CET
    utc_now = datetime.datetime.now(pytz.utc)
    cet_now = utc_now.astimezone(pytz.timezone('CET'))

    current_hour = cet_now.hour
    current_day = cet_now.day

    # Define instance details
    instance_details = [
        {
            "id": "ucw-prd-ec2-bc01.internal.ucw",
            "early_month_type": "r4.xlarge",
            "end_month_type": "c4.8xlarge"
        },
        {
            "id": "ucw-prd-ec2-bc02.internal.ucw",
            "early_month_type": "c4.4xlarge",
            "end_month_type": "c4.8xlarge"
        }
    ]

    for instance in instance_details:
        try:
            # Check instance CPU utilization before modification
            metrics = cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'm1',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EC2',
                                'MetricName': 'CPUUtilization',
                                'Dimensions': [
                                    {
                                        'Name': 'InstanceId',
                                        'Value': instance["id"]
                                    },
                                ]
                            },
                            'Period': 300,
                            'Stat': 'Average',
                        },
                        'ReturnData': True,
                    },
                ],
                StartTime=utc_now - datetime.timedelta(minutes=10),
                EndTime=utc_now,
            )

            cpu_utilization = metrics['MetricDataResults'][0]['Values'][0] if metrics['MetricDataResults'][0]['Values'] else 0
            
            # If CPU utilization is above 20%, it might be actively used (this threshold can be adjusted)
            if cpu_utilization > 20:
                print(f"Instance {instance['id']} is actively used with CPU at {cpu_utilization}%. Skipping modification.")
                continue
            
            if current_day == 1:
                if 0 <= current_hour < 7:  # Before the batch job ends
                    new_instance_type = instance["end_month_type"]
                else:
                    new_instance_type = instance["early_month_type"]
            else:
                new_instance_type = instance["early_month_type"]
            
            # Modify the instance type
            ec2.modify_instance_attribute(
                InstanceId=instance["id"],
                InstanceType={
                    'Value': new_instance_type
                }
            )
            print(f"Instance {instance['id']} changed to {new_instance_type}")

        except Exception as e:
            print(f"Error updating instance {instance['id']}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': "Instances processed successfully!"
    }
