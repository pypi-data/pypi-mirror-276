import computeclient
import re
import json

compute=computeclient.computeclient()
vmname=[]
vmname.append(computeclient.vmname(compute))
result= {}
instancestate={}

#print(f"Test: {vmname}") ## for debug only

def get_vm_ids():
    vmid=[]
    state=compute.virtual_machines.list_all()
    for item in state:
       vmid.append(item.id)
    #print(f"getvmidfunc: {len(vmid)}")   
    return vmid

#store the resource group
def match():
    vmid=get_vm_ids()
    regex=r"\/.*\/resourceGroups\/(.*)\/providers.*\/virtualMachines\/(.*)"
    for i in range(len(vmid)):
        match=re.match(regex,vmid[i])
        resourcegroup=match[1]
        virtualmachine=match[2]
        result[f"resourcegroup_{i}"]=resourcegroup #dictionary add
        result[f"virtualmachine_{i}"]=virtualmachine #dictionar add
    #print(result)
    return result
    #return result

def instanceView():
    vmid=get_vm_ids()
    result=match()
    #print(f"instanceView: {result}")
    for i in range(len(vmid)):
        state=compute.virtual_machines.instance_view(
            resource_group_name=result[f"resourcegroup_{i}"],
            vm_name=result[f"virtualmachine_{i}"]   
        )
        for items in state.statuses:
            if items.display_status.lower() in ["vm running"]:
                #instancestate=f"running",result[f"virtualmachine_{i}"] debug only
                instancestate[f"powerstate_{i}"]=f"running"
            else:
                #instancestate=f"stopped/deallocated",result[f"virtualmachine_{i}"] debug only
                instancestate[f"powerstate_{i}"]=f"stopped/deallocated"
    #print(instancestate)       #print dictionary for debugging
    return instancestate   

def response_body():
        result=match()
        vmid=get_vm_ids()
        instancestate=instanceView()
        response=[]
        for i in range(len(vmid)):
            response.append({
               "message":       f"Deployed virtual machines",
               "vM":            result[f"virtualmachine_{i}"],
               "resourceGroup": result[f"resourcegroup_{i}"],
               "powerState":    instancestate[f"powerstate_{i}"]
            })
            jsonresponse=json.dumps(response)
        #print(f"responsebodyfunc:{jsonresponse}")
        return jsonresponse

def ifStart():
    powerState,vmLocation=instanceView()
    resourcegroup,virtualmachine=match()
    if powerState.lower() in ["deallocated", "stopped", "stopped (deallocated)"]:
        print(f"TET: {powerState}")
        #start the VM
        start=compute.virtual_machines.begin_start(
            resource_group_name=resourcegroup,
            vm_name=virtualmachine
        )
        #check status
        #print("if condition")
        f"Initial poller status: {start.status()}"
        result=start.result()
        f"{result}"
        # Verify if the operation is done
        if start.done():
            f"The operation has completed."
        else:
            f"The operation is still in progress."
    else:
        response = {
            "VM":             f"{virtualmachine}",
            "Resource Group": f"{resourcegroup}",
            "Location":       f"{vmLocation}",
            "VM State":       f"{powerState}",
            "error":          f"Vm is already running"
        }
        jsonresponse=json.dumps(response) #very important step to dump response in JSON for user
        return jsonresponse

if __name__=="__main__":
    instanceView()