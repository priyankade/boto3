# boto3

## Create Role For Lambda Using below Policy for cleanup_ami_sns
````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeImages",
                "ec2:DeregisterImage",
                "ec2:DescribeInstances",
                "ec2:DescribeTags",
                "logs:*",
                "ec2:DescribeImageAttribute",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeInstanceStatus"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:*:<account_id>:<topic_name>"
        }
    ]
}
````
