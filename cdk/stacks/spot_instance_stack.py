from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class SpotInstanceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Use existing VPC or create new one
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        
        # Security Group
        security_group = ec2.SecurityGroup(
            self, "SpotInstanceSG",
            vpc=vpc,
            description="Security group for spot instance",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH"
        )

        # User data (optional)
        user_data = ec2.UserData.for_linux()
        
        # Spot Instance
        spot_instance = ec2.Instance(
            self, "SpotInstance",
            instance_type=ec2.InstanceType("t3.medium"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": "ami-0233e181ab02d7aa3"  # Change region if needed
            }),
            vpc=vpc,
            security_group=security_group,
            user_data=user_data,
            # Spot instance configuration
            instance_market_options=ec2.CfnInstance.InstanceMarketOptionsProperty(
                market_type="spot",
                spot_options=ec2.CfnInstance.SpotOptionsProperty(
                    max_price="0.05",  # Max price per hour
                    spot_instance_type="one-time"  # or "persistent"
                )
            )
        )