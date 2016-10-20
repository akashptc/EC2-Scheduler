import boto3

ec2 = boto3.client('ec2')
instance_ids = []
filters = [{'Name':'tag:Autostop', 'Values':['Yes']}]
i=0

#Filter instances by tags
print "Getting list of Autostop instances..."
instances_list = ec2.describe_instances(Filters=filters)


print len(instances_list['Reservations'])," instances will be stopped"


#Get instance IDs of filtered instances
for instance in instances_list['Reservations']:
	instance_ids.append(instance['Instances'][0]['InstanceId'])

#Stop instances
print "Stopping instances"
ec2.stop_instances(InstanceIds=instance_ids)
