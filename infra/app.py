from aws_cdk import (
    aws_ec2 as ec2,
    core as cdk
)

class MyStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        SduChatBotFront = ec2.CfnInstance(
            self,
            "EC2Instance",
            image_id="ami-0a116fa7c861dd5f9",
            instance_type="t3.small",
            key_name="sdu-chatbot-web-app",
            availability_zone=ec2instance2.attr_availability_zone,
            tenancy="default",
            subnet_id="subnet-0385811b9cc3989bf",
            ebs_optimized=True,
            security_group_ids=[
                "sg-06a375c5cd69f3422"
            ],
            source_dest_check=True,
            block_device_mappings=[
                {
                    "device_name": "/dev/sda1",
                    "ebs": {
                        "encrypted": False,
                        "volume_size": 8,
                        "snapshot_id": "snap-0c84c743eab07c675",
                        "volume_type": "gp3",
                        "delete_on_termination": True
                    }
                }
            ],
            tags=[
                {
                    "key": "Name",
                    "value": "SduChatBot-Front"
                }
            ],
            hibernation_options={
                "configured": False
            },
            cpu_options={
                "core_count": 1,
                "threads_per_core": 2
            },
            enclave_options={
                "enabled": False
            }
        )

        ec2instance2 = ec2.CfnInstance(
            self,
            "EC2Instance2",
            image_id="ami-0a116fa7c861dd5f9",
            instance_type="t3.large",
            key_name="sdu-chatbot-web-app",
            availability_zone="eu-central-1b",
            tenancy="default",
            subnet_id="subnet-0385811b9cc3989bf",
            ebs_optimized=True,
            security_group_ids=[
                "sg-0e62b95986c7d1199"
            ],
            source_dest_check=True,
            block_device_mappings=[
                {
                    "device_name": "/dev/sda1",
                    "ebs": {
                        "encrypted": False,
                        "volume_size": 64,
                        "snapshot_id": "snap-0c84c743eab07c675",
                        "volume_type": "gp3",
                        "delete_on_termination": True
                    }
                }
            ],
            monitoring=True,
            tags=[
                {
                    "key": "Name",
                    "value": "SduChatBot-Back"
                }
            ],
            hibernation_options={
                "configured": False
            },
            cpu_options={
                "core_count": 1,
                "threads_per_core": 2
            },
            enclave_options={
                "enabled": False
            }
        )


app = cdk.App()
MyStack(app, "my-stack-name", env={'region': 'eu-central-1'})
app.synth()
