from azure.identity    import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
import os

#lets make the variables first
tenant_id     =     os.getenv('tenant_id')
client_id     =     os.getenv('client_id')
client_secret =     os.getenv('client_secret')
subid         =     os.getenv('subid')

credentials=ClientSecretCredential(tenant_id=tenant_id,
                                   client_id=client_id,
                                   client_secret=client_secret)

def computeclient():
    compute=ComputeManagementClient(credential=credentials,subscription_id=subid)
    return compute

def vmname(compute):
    vm=compute.virtual_machines.list_all()
    for item in vm:
        name=item.name
    return name 

def returnname(compute):
    name=vmname(compute)
    print(f"VM: {name}")

if __name__=="__main__":
    compute=computeclient()
    returnname(compute)    
