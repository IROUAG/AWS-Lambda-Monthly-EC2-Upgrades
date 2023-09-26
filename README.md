# AWS Lambda Monthly EC2 Upgrades

This repository contains a serverless solution to automate the monthly upgrade and downgrade of Amazon EC2 instances based on specified criteria. The solution is crafted using AWS Lambda, AWS CloudWatch, and Python.

## Overview

The primary function of this script is to:

- Check the current day and time (in CET).
- Based on the time and day, decide whether to upgrade or downgrade specific EC2 instances.
- Before any modifications, ensure the instance is not being actively used (a simple CPU usage check serves as an example in this context).

## Prerequisites

1. **AWS Account**: You need an AWS account to deploy and test this solution.
2. **Python**: The AWS Lambda function is written in Python. Ensure you have the necessary tools to package and deploy a Python-based Lambda function.
3. **pytz Library**: The function uses the `pytz` library to handle time zones. This library needs to be included in the Lambda deployment package.

## AWS Permissions

The Lambda function requires the following permissions:

- **EC2 Permissions**:
  - `ec2:DescribeInstances`: To get the state of EC2 instances.
  - `ec2:ModifyInstanceAttribute`: To change the instance type.
  
- **CloudWatch Permissions**:
  - `cloudwatch:GetMetricData`: To fetch the CPU utilization metric for EC2 instances.

Ensure the IAM role associated with the Lambda function has these permissions.

## Deployment

1. **Lambda Function**: 
   - Navigate to the AWS Lambda console.
   - Create a new Lambda function and choose Python as the runtime.
   - Upload the function code and include the `pytz` library in the deployment package.
   
2. **Scheduling**:
   - Use AWS EventBridge (CloudWatch Events) to schedule the Lambda function. It's recommended to schedule the function around the specific times when you want the instances to be upgraded or downgraded.

3. **Monitoring**:
   - Use AWS CloudWatch to monitor the logs and metrics of the Lambda function.

## Contribution

Feel free to fork this repository and make any adjustments or enhancements. Pull requests are welcome!

## License

This project is open source and available under the [MIT License](LICENSE).
