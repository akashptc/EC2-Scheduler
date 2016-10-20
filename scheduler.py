import boto3

ec2 = boto3.client('ec2')
instance_ids = []
filters = [{'Name':'tag:Autostop', 'Values':['Yes']}]

#Filter instances by tags
instances_list = ec2.describe_instances(Filters=filters)

#Get instance IDs of filtered instances
for instances in instances_list:
	instance_ids.append(instances_list['Reservations'][0]['Instances'][0]['InstanceId'])

#Stop instances
ec2.stop_instances(InstanceIds=instance_ids)
