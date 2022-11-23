import json
from time import sleep
import ast
import os

def change_permission(dir_path, sudoPassword):
    paths = dir_path.split('/')
    for i in range(2, len(paths)+1):
        path = '/'.join(paths[:i])

        # 若 path permission 已經為 777, 則不用改變他的 permission
        if oct(os.stat(path).st_mode)[-3:] == '777':
            continue

        if i != len(paths):
            changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 {path}"
            os.system(changePermission_cmd)
        else:
            changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {path}"
            os.system(changePermission_cmd)
def usbdf():
    port_state = {}
    usb_file = open('/home/server/dash_brain/usb_data/usb.json', 'w', newline='')
    cdb=open("/home/server/dash_brain/usb_data/usb_cdb.json","r")
    cdb_line=cdb.readlines()
    change_permission("/var/ossec/logs/alerts/alerts.json","0314")
    with open("/var/ossec/logs/alerts/alerts.json","r") as jsonfiles:
        lines=jsonfiles.readlines()
        usb_detail={}
        usb2json = {}
        for line in lines:
            info=json.loads(line)
            #print(info["rule"]["id"])
            if info["rule"]["id"]=='81104' and info["location"]=='/var/log/kern.log':
                usb_detail["In_Date"]=info["timestamp"].split("T")[0]
                usb_detail["In_Time"]=info["timestamp"].split("T")[1].split(".")[0]
                usb_detail["Out_Date"]='-'
                usb_detail["Out_Time"]='-'
                usb_detail["agent_id"]=info["agent"]["id"]
                usb_detail["agent_name"]=info["agent"]["name"]
                usb_detail["authorized"]="black"
                full_log=info["full_log"].split(" ")
                usb_detail["SerialNum"]=full_log[-1]
                #print("dsds")
                if "SerialNumber" not in usb_detail["SerialNum"]:
                    for cline in cdb_line:
                        cline = ast.literal_eval(cline)
                        if usb_detail["SerialNum"] == cline["cdb_SN"] and cline["Aid"] == usb_detail["agent_id"]:
                            usb_detail["authorized"]="white"
                    #print("偵測到USB~")
                    #print(usb_detail["SerialNum"])
                    usb_port=full_log[-3].strip(":")
                    usb_detail["connected"] = 1
                    usb_detail["UsbPort"]=full_log[-3].strip(":")
                    print(usb_detail)
                    port_state[usb_port] = usb_detail.copy()
                    #print("insert:\n",port_state)
                    
            if info["rule"]["id"]=='81102' and info["location"]=='/var/log/kern.log':
                #print("boy")
                full_log=info["full_log"].split(" ")
                usb_port_exit=full_log[-6].strip(":")
                #print(usb_port_exit)
                #print(port_state)
                try:
                    port_state[usb_port_exit]["Out_Date"] = info["timestamp"].split("T")[0]
                    port_state[usb_port_exit]["Out_Time"] = info["timestamp"].split("T")[1].split(".")[0]
                    port_state[usb_port_exit]["connected"]=0
                    json.dump(port_state[usb_port_exit], usb_file)
                    usb_file.write('\n')
                #print(usb_port_exit)
                except:
                    print("drop")
                
                #print("outsert:\n",port_state)
    for _, state in port_state.items():
        if state["connected"] == 1:
            json.dump(state, usb_file)
            usb_file.write('\n')
    usb_file.close()

    usb_info=open('/home/server/dash_brain/usb_data/usb_info.json',"w", newline='')
    usb_info.write("[")
    f=open('/home/server/dash_brain/usb_data/usb.json',"r")
    lines=f.readlines()
    check=len(lines)
    #print(check)
    i=0
    for line in lines:
        line = ast.literal_eval(line)
        json.dump(line,usb_info)
        if i != check-1:
            usb_info.write(",")
        i+=1
    usb_info.write("]")
    usb_info.close()
    f.close()
usbdf()