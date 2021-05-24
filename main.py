import boto3

# Global variables, please fill with the correct information from the ASAv's
# =========================================================
asav_active = "i-abcdef"
eni_active_inside = "eni-aaaaaa"
eni_active_outside = "eni-bbbbbb"
active_priavteIP_outside = "172.16.2.20"

eni_standby_inside = "eni-cccccc"
eni_standby_outside = "eni-dddddd"
standby_privateIP_outside = "172.16.4.20"

active_publicIP = "54.54.54.1"
active_publicIP_allocationId = "eipalloc-aaaaaa"
standby_publicIP = "54.54.54.2"
standby_publicIP_allocationId = "eipalloc-bbbbbb"
# =========================================================
# End of Global Variables

# Here we are calling the ec2 client SDK from boto3
client = boto3.client('ec2')

# We will filter only the route tables that have routes pointing to the active ASAvA
route_tables = client.describe_route_tables(Filters=[{'Name': 'route.instance-id','Values': [asav_active]}])
# This variable will save the number of route tables
n = len(route_tables['RouteTables'])
# Now we will iterate through each route table
for i in range(n):
    # This variable will save the route table id for later execution
    routeid = route_tables['RouteTables'][i]['RouteTableId']
    # This variable will save the number of route entries within the route table
    m = len(route_tables['RouteTables'][i]['Routes'])
    # Now we will iterate through each route entry
    for j in range(m):
        # This variable will save the route entry for comparison
        route = route_tables['RouteTables'][i]['Routes'][j]
        # We need this because not all the route entries have NetworkInterfaceId as the gateway, so we avoid those errors
        try:
            # We compare now if the NetworkInterfaceId is tha same as the active ASA, and if it is the case, we proceed to replace the route entry with the new ASAvB
            if route['NetworkInterfaceId'] == eni_active_inside:
                destination = route['DestinationCidrBlock']
                client.replace_route(
                    DestinationCidrBlock=destination,
                    NetworkInterfaceId=eni_standby_inside,
                    RouteTableId=routeid)
        except KeyError:
            continue
# In this last section we are swapping the public EIP's from both ASAv's outside interfaces
client.disassociate_address(
    PublicIp=active_publicIP)

client.disassociate_address(
    PublicIp=standby_publicIP)

client.associate_address(
    AllocationId=active_publicIP_allocationId,
    NetworkInterfaceId=eni_standby_outside,
    PrivateIpAddress=standby_privateIP_outside)

client.associate_address(
    AllocationId=standby_publicIP_allocationId,
    NetworkInterfaceId=eni_active_outside,
    PrivateIpAddress=active_priavteIP_outside)
