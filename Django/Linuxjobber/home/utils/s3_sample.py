#!/bin/python

import boto3
import uuid
import sys
from botocore.exceptions import ClientError
 
####################### How to find new centos ami_ID
# CentOS publishes their AMI product codes to their wiki:https://wiki.centos.org/Cloud/AWS. It provides the following information for the latest CentOS 7 AMI:
#     Owner: aws-marketplace
#     Product Code: aw0evgkw8e5c1q413zgy5pjce
# The run this to get the awsID:
# #aws ec2 describe-images --owners 'aws-marketplace' --filters 'Name=product-code,Values=aw0evgkw8e5c1q413zgy5pjce' --query 'sort_by(Images, &CreationDate)[-1].[ImageId]' --output 'text'
######################

ACCESS_KEY=sys.argv[1]
SECRET_KEY=sys.argv[2]
ACTION_TYPE=sys.argv[3]
if len( sys.argv) > 4:
    RESOURCE_ID=sys.argv[4]

# Determine which region this user is using
#try west coast first. If the user does not have vpc in west coast, then he/she must be in the east coast
try:
    rds = boto3.setup_default_session(region_name='us-west-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    ec2 = boto3.resource('ec2')
    ec2sg = boto3.client('ec2')
    response = ec2sg.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
except IndexError as ie:
    print(ie) 
    rds = boto3.setup_default_session(region_name='us-east-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    ec2 = boto3.resource('ec2')
    ec2sg = boto3.client('ec2')
    response = ec2sg.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
except ClientError as ce:
    print(ce)
    sys.exit(1)

secgid=''

if ACTION_TYPE=='launch_instance':
    try:
        response = ec2sg.create_security_group(GroupName='lj_sec_group',
                                             Description='LinuxjobberSecurityGroup',
                                             VpcId=vpc_id)
        secgid = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (secgid, vpc_id))

        data = ec2sg.authorize_security_group_ingress(
            GroupId=secgid,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 58500,
                 'ToPort': 58500,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)

# Find the security group id for lj_sec_group. It must exist at this point. If it doesn't, fix code above to ensure it exist before going past this point
all_sg = ec2sg.describe_security_groups()
for i in all_sg['SecurityGroups']:
    if str(i['GroupName']) == 'lj_sec_group':
        secgid=str(i['GroupId'])
    if not (ACTION_TYPE=='instance_running' or ACTION_TYPE=='instance_stopped') :
    #for j in i['Description']:
    #    print('Security group info: '+str(j['Description']))# +str(j['PrefixListIds'])) #+str(j['GroupName'])+str(j['GroupId']))
        print ('==============================\n')
        print ( 'group name: ' + str(i['GroupName']))
        print ( 'group id: ' + str(i['GroupId']))
        print ( 'group description: ' + str(i['Description'])+str(i['IpPermissions']) + '\n')








#outfile = open('TestKey4.pem','w')
#key_pair = ec2.create_key_pair(KeyName='TestKey4')
#KeyPairOut = str(key_pair.key_material)
#outfile.write(KeyPairOut)


ACCESS_SCRIPT="""#!/bin/bash
/usr/bin/sed -i -e 's/PasswordAuthentication\ no/PasswordAuthentication\ yes/g' /etc/ssh/sshd_config
/sbin/useradd -p $( /usr/bin/echo '8iu7*IU&' | openssl passwd -1 -stdin) sysadmin
echo 'sysadmin  ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers
echo 'shopt -s histappend' >> /home/sysadmin/.bashrc
echo 'export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"' >> /home/sysadmin/.bashrc
/usr/bin/systemctl restart sshd.service
"""

if ACTION_TYPE=='verify':
    instances = ec2.instances.all()
elif ACTION_TYPE=='describe_instance':
    response = ec2sg.describe_instances()
elif ACTION_TYPE=='start_instance':
    instances = ec2.instances.filter(InstanceIds=[RESOURCE_ID]).start()
elif ACTION_TYPE=='stop_instance':
    instances = ec2.instances.filter(InstanceIds=[RESOURCE_ID]).stop()
elif ACTION_TYPE=='terminate_instance':
    instances = ec2.instances.filter(InstanceIds=[RESOURCE_ID]).terminate()
elif ACTION_TYPE=='instance_running':
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
elif ACTION_TYPE=='instance_stopped':
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
elif ACTION_TYPE=='launch_instance':
    #instances = ec2.create_instances(ImageId='ami-18f8df7d', SecurityGroupIds=['default'], MinCount=1, MaxCount=1, KeyName='TestKey4', InstanceType='t2.micro')
    #instances = ec2.create_instances(ImageId='ami-18f8df7d', SecurityGroupIds=['default'], MinCount=1, MaxCount=1, KeyName='TestKey4', InstanceType='t2.micro', UserData=ACCESS_SCRIPT)
    try:
        try:
            instances = ec2.create_instances(ImageId='ami-0ebdd976', SecurityGroupIds=[secgid], MinCount=1, MaxCount=1, InstanceType='t2.micro', UserData=ACCESS_SCRIPT)
        except NameError:
            instances = ec2.create_instances(ImageId='ami-223f945a', SecurityGroupIds=[secgid], MinCount=1, MaxCount=1, InstanceType='t2.micro', UserData=ACCESS_SCRIPT)
    except ClientError as e:
        if "You are not subscribed to this service" in str(e):
            print ("permission denied for service")
        elif "Not authorized for images" in str(e):
            print ("permission denied for image")
        else:
            print (e)
        sys.exit(1)


if ACTION_TYPE=='verify':
    try:
        for instance in instances:
            print( instance.id)
    except:
        print( "no instances found")

elif ACTION_TYPE=='describe_instance':
    for r in response['Reservations']:
        for i in r['Instances']:
            print (i['InstanceId'], i['Hypervisor'])
            for b in i['BlockDeviceMappings']:
                print (b['Ebs']['DeleteOnTermination'])
elif ACTION_TYPE=='start_instance':
    for instance in instances:
        print( instance.get('StartingInstances')[0].get('InstanceId'),  instance.get('StartingInstances')[0].get('CurrentState').get('Name'))
elif ACTION_TYPE=='stop_instance':
    for instance in instances:
        print( instance.get('StoppingInstances')[0].get('InstanceId'),  instance.get('StoppingInstances')[0].get('CurrentState').get('Name'))
elif ACTION_TYPE=='terminate_instance':
    for instance in instances:
        print( instance.get('TerminatingInstances')[0].get('InstanceId'),  instance.get('TerminatingInstances')[0].get('CurrentState').get('Name'))
elif ACTION_TYPE=='instance_running':
    for instance in instances:
        print( '%s %s,' %(instance.id, instance.public_ip_address))
elif ACTION_TYPE=='instance_stopped':
    for instance in instances:
        print( '%s %s,' %(instance.id, instance.public_ip_address))
else:
    for instance in instances:
        try:
            print( 'instance_id='+instance.id, 'instance_tag='+instance.tags[0].get('Value'), 'instance_ip='+instance.public_ip_address)
        except TypeError:
            try:
                print( 'instance_id='+instance.id, 'instance_ip='+instance.public_ip_address, instance.security_groups)
            except TypeError:
                    try:
                        print( 'instance_id='+instance.id, 'instance_tag='+instance.tags[0].get('Value'))
                    except ValueError:
                        print( 'instance_id='+instance.id)
                    except TypeError:
                        print( 'instance_id='+instance.id)


 
