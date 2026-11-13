from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct

class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        self.vpc = ec2.Vpc(
            self, "SduChatBotVPC",
            vpc_name="SduChatBot-VPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

        # Frontend Security Group
        self.frontend_sg = ec2.SecurityGroup(
            self, "FrontendSG",
            vpc=self.vpc,
            security_group_name="SduChatBot-Frontend-SG",
            description="Security group for Frontend instances",
            allow_all_outbound=True
        )

        # Frontend rules
        self.frontend_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "SSH access"
        )
        self.frontend_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "HTTP access"
        )
        self.frontend_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "HTTPS access"
        )

        # Backend Security Group
        self.backend_sg = ec2.SecurityGroup(
            self, "BackendSG",
            vpc=self.vpc,
            security_group_name="SduChatBot-Backend-SG",
            description="Security group for Backend instances",
            allow_all_outbound=True
        )

        # Backend rules
        self.backend_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "SSH access"
        )
        
        # Backend API - only from Frontend SG (more secure)
        self.backend_sg.add_ingress_rule(
            ec2.Peer.security_group_id(self.frontend_sg.security_group_id),
            ec2.Port.tcp(8000),
            "API access from Frontend"
        )
        
        # Optional: Allow direct API access from anywhere (less secure)
        # Uncomment if you need direct backend access
        # self.backend_sg.add_ingress_rule(
        #     ec2.Peer.any_ipv4(),
        #     ec2.Port.tcp(8000),
        #     "API direct access"
        # )

        # Outputs
        CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
        CfnOutput(self, "FrontendSecurityGroupId", value=self.frontend_sg.security_group_id)
        CfnOutput(self, "BackendSecurityGroupId", value=self.backend_sg.security_group_id)
        CfnOutput(
            self, "PublicSubnetIds",
            value=",".join([subnet.subnet_id for subnet in self.vpc.public_subnets])
        )
        CfnOutput(
            self, "PrivateSubnetIds",
            value=",".join([subnet.subnet_id for subnet in self.vpc.private_subnets])
        )