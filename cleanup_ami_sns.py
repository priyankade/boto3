import boto3

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

instances = ec2.describe_instances()

def lambda_handler(event, context):
    used_ami = []  # Create empty list to save used ami
    
    ###Finding used ami ID list, do not deregister these
    #Append running instances' image id in the used_ami list
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']
            state = state['Name']
            if state == 'running':
                used_ami.append(instance['ImageId'])

    #Remove duplicates using set
    #used ami ID list
    used_ami = list(set(used_ami))

    #  print(f"The used amis are: {used_ami}")
    #  print("check")

    ###Finding all available images list
    available_images = ec2.describe_images(
                    Filters=[
                        {
                            'Name': 'state',
                            'Values': [
                                'available',
                            ]
                        },
                    ],
                    Owners=[
                        'self',
                    ]
                )
    # print("All available images : {}".format(available_images))

    #available ami ID list
    all_images = []
    for image in available_images['Images']:
        all_images.append(image['ImageId'])

    print("All available images IDs : {}".format(all_images))

    #Deregistering unused amis
    deregistered_ami = []
    for ami in all_images:
        if ami not in used_ami:
            print("Deregistering unused amis: {}".format(ami))

            ec2.deregister_image( ImageId=ami,
                                        DryRun=True
                                    )

            deregistered_ami.append(ami)
        
    #SNS
    sns.publish(
                        TopicArn='arn:aws:sns:us-east-1:************:Notify-unused-AMI',
                        Subject='Alert - Unused AMI deregistered',
                        Message=str(deregistered_ami)
                    ) 
    
    return("success")
