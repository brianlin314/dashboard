import json
cdbtxt=open("/home/server/dash_brain/usb_data/usb_cdb.txt","r")
cdbjson=open("/home/server/dash_brain/usb_data/usb_cdb.json","w")
clines=cdbtxt.readlines()
cdb_temp={}
for line in clines:
    line=line.strip()
    print(line)
    cdb_temp["cdb_SN"]=line
    json.dump(cdb_temp,cdbjson)
    cdbjson.write("\n")
cdbjson.close()
cdbtxt.close()