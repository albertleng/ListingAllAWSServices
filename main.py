import os
import boto3
import logging
from botocore.exceptions import ClientError
from datetime import datetime
import glob

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("aws_services.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()

OwnerTagValue = os.environ.get('OwnerTagValue', 'AlbertLeng')


def list_my_ec2_instances():
    logger.info("Listing EC2 instances...")
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Owner', 'Values': [OwnerTagValue]}
        ]
    )
    ec2_info = [{'InstanceId': instance['InstanceId'],
                 'State': instance['State']['Name']}
                for reservation in instances['Reservations'] for instance in
                reservation['Instances']]
    return ec2_info


def list_my_rds_instances():
    logger.info("Listing RDS instances...")
    rds_client = boto3.client('rds')
    instances = rds_client.describe_db_instances()
    my_rds_info = []
    for instance in instances['DBInstances']:
        tags = rds_client.list_tags_for_resource(
            ResourceName=instance['DBInstanceArn'])
        for tag in tags['TagList']:
            if tag['Key'] == 'Owner' and tag['Value'] == OwnerTagValue:
                my_rds_info.append({
                    'DBInstanceIdentifier': instance['DBInstanceIdentifier'],
                    'DBInstanceStatus': instance['DBInstanceStatus']
                })
                break
    return my_rds_info


def list_my_ecs_services():
    logger.info("Listing ECS services...")
    ecs_client = boto3.client('ecs')
    clusters = ecs_client.list_clusters()['clusterArns']
    ecs_info = []
    for cluster_arn in clusters:
        services = ecs_client.list_services(cluster=cluster_arn)['serviceArns']
        for service_arn in services:
            tags = ecs_client.list_tags_for_resource(resourceArn=service_arn)
            for tag in tags['tags']:
                if tag['key'] == 'Owner' and tag['value'] == OwnerTagValue:
                    ecs_info.append(
                        {'ClusterArn': cluster_arn, 'ServiceArn': service_arn})
                    break
    return ecs_info


def list_my_ebs_volumes():
    logger.info("Listing EBS volumes...")
    ec2_client = boto3.client('ec2')
    volumes = ec2_client.describe_volumes(
        Filters=[
            {'Name': 'tag:Owner', 'Values': [OwnerTagValue]}
        ]
    )
    ebs_info = [{'VolumeId': volume['VolumeId'], 'State': volume['State'],
                 'Size': volume['Size']}
                for volume in volumes['Volumes']]
    return ebs_info


def list_my_s3_buckets():
    logger.info("Listing S3 buckets...")
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()
    my_s3_info = []
    for bucket in buckets['Buckets']:
        try:
            tags = s3_client.get_bucket_tagging(Bucket=bucket['Name'])
            for tag in tags['TagSet']:
                if tag['Key'] == 'Owner' and tag['Value'] == OwnerTagValue:
                    my_s3_info.append({'BucketName': bucket['Name']})
                    break
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                continue
            else:
                raise e
    return my_s3_info


def list_my_security_groups():
    logger.info("Listing security groups...")
    ec2_client = boto3.client('ec2')
    security_groups = ec2_client.describe_security_groups(
        Filters=[
            {'Name': 'tag:Owner', 'Values': [OwnerTagValue]}
        ]
    )
    sg_info = [{'GroupId': sg['GroupId'], 'GroupName': sg['GroupName']} for sg
               in security_groups['SecurityGroups']]
    return sg_info


def list_my_key_pairs():
    logger.info("Listing key pairs...")
    ec2_client = boto3.client('ec2')
    key_pairs = ec2_client.describe_key_pairs(
        Filters=[
            {'Name': 'tag:Owner', 'Values': [OwnerTagValue]}
        ]
    )
    kp_info = [
        {'KeyName': kp['KeyName'], 'KeyFingerprint': kp['KeyFingerprint']} for
        kp in key_pairs['KeyPairs']]
    return kp_info


def list_my_iam_roles():
    logger.info("Listing IAM roles...")
    iam_client = boto3.client('iam')
    roles = iam_client.list_roles()
    my_iam_info = []
    for role in roles['Roles']:
        tags = iam_client.list_role_tags(RoleName=role['RoleName'])
        for tag in tags['Tags']:
            if tag['Key'] == 'Owner' and tag['Value'] == OwnerTagValue:
                my_iam_info.append(
                    {'RoleName': role['RoleName'], 'RoleId': role['RoleId']})
                break
    return my_iam_info


def delete_existing_txt_files():
    logger.info("Deleting existing .txt files...")
    txt_files = glob.glob('*.txt')
    for file in txt_files:
        os.remove(file)
        logger.info(f"Deleted {file}")


def write_to_file(filename, data, service_name):
    if data:
        logger.info(f"Writing {service_name} data to {filename}...")
        with open(filename, 'a') as file:
            file.write(f'{service_name}:\n')
            for item in data:
                file.write(str(item) + '\n')
            file.write('\n')
    else:
        logger.info(f"No {service_name} found.")


def main():
    delete_existing_txt_files()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'{timestamp}_all_my_instances_services.txt'

    ec2_info = list_my_ec2_instances()
    rds_info = list_my_rds_instances()
    ecs_info = list_my_ecs_services()
    ebs_info = list_my_ebs_volumes()
    s3_info = list_my_s3_buckets()
    sg_info = list_my_security_groups()
    kp_info = list_my_key_pairs()
    iam_info = list_my_iam_roles()

    write_to_file('my_ec2_instances.txt', ec2_info, 'EC2 Instances')
    write_to_file('my_rds_instances.txt', rds_info, 'RDS Instances')
    write_to_file('my_ecs_services.txt', ecs_info, 'ECS Services')
    write_to_file('my_ebs_volumes.txt', ebs_info, 'EBS Volumes')
    write_to_file('my_s3_buckets.txt', s3_info, 'S3 Buckets')
    write_to_file('my_security_groups.txt', sg_info, 'Security Groups')
    write_to_file('my_key_pairs.txt', kp_info, 'Key Pairs')
    write_to_file('my_iam_roles.txt', iam_info, 'IAM Roles')

    with open(output_filename, 'w') as f:
        f.write('')

    write_to_file(output_filename, ec2_info, 'EC2 Instances')
    write_to_file(output_filename, rds_info, 'RDS Instances')
    write_to_file(output_filename, ecs_info, 'ECS Services')
    write_to_file(output_filename, ebs_info, 'EBS Volumes')
    write_to_file(output_filename, s3_info, 'S3 Buckets')
    write_to_file(output_filename, sg_info, 'Security Groups')
    write_to_file(output_filename, kp_info, 'Key Pairs')
    write_to_file(output_filename, iam_info, 'IAM Roles')

    logger.info(f"Service information has been written to {output_filename}.")


if __name__ == '__main__':
    main()
