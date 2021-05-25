# ASAv Failover in AWS

Hi! This code was created as a workaround since Cisco ASAv failover in AWS is not possible due to L2 (Layer 2) limitations.

## What the code does?

This code basically replaces all the route entries that are pointing to the active ASAvA to the backup ASAvB performing an automatic failover. It also swaps the public EIP's (Elastic IP's) over the outside interfaces of both ASAv's.

## Global variables

Please make sure you fill the variables with the correct information, otherwise the code won't work as expected.

## How I trigger this code?

It can be triggered locally if you have the keys and the permissions configured, but the idea is to implement it in conjunction with other AWS services like CloudWatch, SNS and Lambda to automate the process.

## Any dependencies?

This code is compatible with python3 and it uses boto3, you can find more information here: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

## Can I help to improve the code?

Sure, this will be a public repository, and any contribution will be reviewed and added accordingly.
