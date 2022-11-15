import pandas as pd
from database import get_db
from datetime import date

def initialize():
    global posts, num, first, agent_pi_ip1, agent_pc_ip1, current_db, selected_fields, add_next_click, all_fields, fields_num, agent_pi_ip , agent_pc_ip, hidsdirpath, nidsdirpath, agent_pi_id , agent_pc_id, pcapdirpath, csvdirpath, modelpath
    # 需要 sudo 密碼以存取檔案
    today = date.today()
    agent_pc_id = "000"
    agent_pi_id = "001"
    agent_pi_ip = "192.168.65.77:0"
    agent_pi_ip1 = "192.168.65.77"
    agent_pc_ip = '192.168.65.65:8'
    agent_pc_ip1 = '192.168.65.65'
    sudoPassword = '0314' # 0
    dir_path = '/var/ossec/logs/alerts'
    hidsdirpath = '/var/ossec/logs/alerts/' #('放你的wazuhlog存放路徑 不包含年月日'+'/'+today.year+'/'+today.strftime("%b")+'/ossec-alerts-'+today.day+'.json')
    nidsdirpath = '/var/log/suricata/'  #nids存放路徑 不包含檔名
    pcapdirpath = '/home/server/wirepcap/pcap/'
    csvdirpath= '/home/server/wirepcap/csv/'
    modelpath = '/home/server/dash/components/pima.pickle.dat'
    selected_fields = []
    client, posts, num, current_db, = get_db.get_current_db(dir_path, sudoPassword)
    all_fields, fields_num = get_fields(posts)
    add_next_click = [1 for i in range(fields_num)]

def get_fields(posts):
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)
    all_fields = list(df.columns)
    all_fields.remove('timestamp')
    return all_fields, len(all_fields)
