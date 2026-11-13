import aws_cdk as cdk
from spot_instance_stack import SpotInstanceStack

app = cdk.App()
SpotInstanceStack(app, "SpotInstanceStack")
app.synth()