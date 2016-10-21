import boto3
import time
import datetime
import sys

ec2res = boto3.resource('ec2')
ec2 = boto3.client('ec2')
instance_ids = []
filters = [{'Name':'tag:Autostop', 'Values':['Yes']}]
logfile = open('scheduler-log.txt', 'a')

try:
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

	#Waiting for instances to stop
	for id in instance_ids:
		instance = ec2res.Instance(id)
		while(instance.state['Name']!="stopped"):
			time.sleep(3)
			instance.reload()
			instance_status = instance.state['Name']
			print instance.state['Name'], id

	#Write logs
	timestamp = str(datetime.datetime.utcnow())
	logfile.write("\n---Stopping Instances---")
	logfile.write(timestamp)
	logfile.write("---\n")
	logfile.write("Instances stopped:\n")
	logfile.write(str(instance_ids))
	logfile.write("\nSuccess")
	logfile.close()

except:
	e = sys.exc_info()[0]
	logfile.write("\nError: \n"),e
	logfile.close()
