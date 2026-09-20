import urllib.request
import boto3

REGION='us-east-1'
KEY_NAME='retail_pipeline_key'
KEY_FILE=f'{KEY_NAME}.pem'
SECURITY_GROUP_NAME='retail_pipeline_sg'
INSTANCE_NAME='retail_pipeline_ec2'
INSTANCE_TYPE='t3.micro'

ec2=boto3.client('ec2',region_name=REGION)

def get_my_ip():
    response=urllib.request.urlopen('https://checkip.amazonaws.com')
    ip=response.read().decode().strip()
    return f'{ip}/32'

def create_key_pair():
    try:
        response=ec2.create_key_pair(KeyName=KEY_NAME)
        with open(KEY_FILE,'w') as f:
            f.write(response['KeyMaterial'])
        print(f"Created key pair, saved to {KEY_FILE}")
        print("Keep this file safe - anyone with it can SSH into your instance.")
    except ec2.exceptions.ClientError as e:
        if 'InvalidKeyPair.Duplicate' in str(e):
            print(f"Key pair '{KEY_NAME}' already exists, reusing it.")
        else:
            raise

def get_or_create_security_group():
    my_ip=get_my_ip()
    print(f"Your public IP: {my_ip}")
    
    existing=ec2.describe_security_groups(
        Filters=[{
            "Name":"group-name",
            "Values":[SECURITY_GROUP_NAME]
        }]
    )
    
    if existing['SecurityGroups']:
        sg=existing['SecurityGroups'][0]
        sg_id=sg['GroupId']
        print(f"Security group already exists: {sg_id}")
        
        old_ssh_rule=[
            perm for perm in sg['IpPermissions']
            if perm.get('FromPort')==22 and perm.get('ToPort')==22
        ]
        
        if old_ssh_rule:
            ec2.revoke_security_group_ingress(GroupId=sg_id,IpPermissions=old_ssh_rule)
            print("  removed old SSH rule(s)")
    
    else:
        vpcs = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])
        vpc_id = vpcs["Vpcs"][0]["VpcId"]
    
        sg=ec2.create_security_group(
            GroupName=SECURITY_GROUP_NAME,
            Description='Allows SSH only from my IP - retail pipeline project',
            VpcId=vpc_id
        )
    
        sg_id=sg['GroupId']
        print(f"Created new security group: {sg_id}")
    
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol":'tcp',
                'FromPort':22,
                'ToPort':22,
                'IpRanges':[{'CidrIp':my_ip,'Description':'SSH from my IP'}]
            }
        ]
    )
    
    print(f"(SSH allowed only from {my_ip})")
    return sg_id

def get_latest_amazon_linux_ami():
    response = ec2.describe_images(
        Owners=["amazon"],
        Filters=[
            {"Name": "name", "Values": ["al2023-ami-*-x86_64"]},
            {"Name": "state", "Values": ["available"]},
        ],
    )
    # Sort by creation date, take the newest
    images = sorted(response["Images"], key=lambda x: x["CreationDate"], reverse=True)
    ami_id = images[0]["ImageId"]
    print(f"Using AMI: {ami_id} ({images[0]['Name']})")
    return ami_id

def launch_instance(sg_id,ami_id):
    response=ec2.run_instances(
        ImageId=ami_id,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SecurityGroupIds=[sg_id],
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType':'instance',
                'Tags':[{
                    'Key':'Name',
                    'Value':INSTANCE_NAME
                }]
            }
        ]
    )
    
    instance_id=response['Instances'][0]['InstanceId']
    print(f"Launched instance: {instance_id}")
    print("Waiting for it to enter 'running' state...")
    
    waiter=ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    
    described=ec2.describe_instances(InstanceIds=[instance_id])
    public_ip=described['Reservations'][0]['Instances'][0].get('PublicIpAddress')
    
    print(f"\n✅ Instance is running!")
    print(f"Instance ID: {instance_id}")
    print(f"Public IP: {public_ip}")
    print(f"\nTo connect via SSH:")
    print(f"  ssh -i {KEY_FILE} ec2-user@{public_ip}")
    
    return instance_id

create_key_pair()
sg_id=get_or_create_security_group()
ami_id=get_latest_amazon_linux_ami()
launch_instance(sg_id,ami_id)
    