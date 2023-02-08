import pandas as pd
from database import get_db, get_ndb
from datetime import date

def initialize():
    global posts, num, sudoPassword, first, agent_pi_ip1, agent_pc_ip1, current_db, selected_fields, hposts, hnum, current_hdb, n_selected_fields, add_next_click, all_fields, fields_num, hadd_next_click, all_hfields, hfields_num, agent_pi_ip , agent_pc_ip, hidsdirpath, nidsdirpath, agent_pi_id , agent_pc_id, pcapdirpath, csvdirpath, modelpath
    # 需要 sudo 密碼以存取檔案
    today = date.today()
    agent_pc_id = "004"
    agent_pi_id = "003"
    agent_pi_ip = "192.168.3.66:80"
    agent_pi_ip1 = "192.168.3.66"
    agent_pc_ip = '192.168.3.7:80'
    agent_pc_ip1 = '192.168.3.7'
    sudoPassword = '0314' # 0
    dir_path = '/var/ossec/logs/alerts'
    hidsdirpath = '/var/ossec/logs/alerts/' #('放你的wazuhlog存放路徑 不包含年月日'+'/'+today.year+'/'+today.strftime("%b")+'/ossec-alerts-'+today.day+'.json')
    nidsdirpath = '/var/log/suricata/'  #nids存放路徑 不包含檔名
    pcapdirpath = '/home/server/wirepcap/pcap/'
    csvdirpath= '/home/server/wirepcap/csv/'
    modelpath = '/home/server/dash/components/pima.pickle.dat'
    selected_fields = []
    n_selected_fields = []
    client, posts, num, current_db, = get_db.get_current_db(dir_path, sudoPassword)
    # hclient, hposts, hnum, current_hdb, = get_ndb.get_current_db(nidsdirpath, sudoPassword)
    all_fields, fields_num = get_fields(posts)
    # all_hfields, hfields_num = get_hfields(hposts)
    add_next_click = [1 for i in range(fields_num)]
    # hadd_next_click = [1 for i in range(hfields_num)]

def get_fields(posts):
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)
    all_fields = list(df.columns)
    all_fields.remove('timestamp')
    return all_fields, len(all_fields)

def get_hfields(posts):
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)
    all_hfields = list(df.columns)
    all_hfields.remove('timestamp')
    return all_hfields, len(all_hfields)
