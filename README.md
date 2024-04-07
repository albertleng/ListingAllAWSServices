# AWS Services Inventory Script

## Overview
This Python script provides a comprehensive inventory of various AWS resources owned by a specific user. It lists EC2 instances, RDS instances, ECS services, EBS volumes, S3 buckets, security groups, key pairs, and IAM roles tagged with a specific owner tag value. The script generates individual text files for each resource type as well as a consolidated file containing all the information.

## Prerequisites
- Python 3.x
- Boto3 library
- AWS CLI configured with appropriate credentials and default region
- An environment variable `OwnerTagValue` set to the owner tag value for filtering resources

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install the Boto3 library using pip:
```
pip install boto3
```
3. Configure the AWS CLI with your credentials and default region:
```
aws configure
```
4. Set the `OwnerTagValue` environment variable to the desired owner tag value:
```
export OwnerTagValue="YourOwnerTagValue"
```


## Usage
Run the script using Python:
```
python main.py
```


The script will generate the following files in the current directory:
- `my_ec2_instances.txt`: List of EC2 instances tagged with the specified owner tag value.
- `my_rds_instances.txt`: List of RDS instances tagged with the specified owner tag value.
- `my_ecs_services.txt`: List of ECS services tagged with the specified owner tag value.
- `my_ebs_volumes.txt`: List of EBS volumes tagged with the specified owner tag value.
- `my_s3_buckets.txt`: List of S3 buckets tagged with the specified owner tag value.
- `my_security_groups.txt`: List of security groups tagged with the specified owner tag value.
- `my_key_pairs.txt`: List of key pairs tagged with the specified owner tag value.
- `my_iam_roles.txt`: List of IAM roles tagged with the specified owner tag value.
- `[timestamp]_all_my_instances_services.txt`: Consolidated file containing all the above information.

## Logging
The script logs its progress and any errors encountered to both the console and a file named `aws_services.log` in the current directory.

## Note
- The script assumes that the resources are tagged with a tag key `Owner` and the corresponding value is set in the `OwnerTagValue` environment variable.
- Ensure that the AWS credentials used have the necessary permissions to list and describe the resources.

## Author
Albert Leng
