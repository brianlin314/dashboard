import pandas as pd
from database import get_db
from datetime import date

def initialize():
    global posts, num, first, current_db, selected_fields, add_next_click, all_fields, fields_num, agent_pi_ip , agent_pc_ip, hidsdirpath, nidsdirpath, agent_pi_id , agent_pc_id, pcapdirpath, csvpath, modelpath
    # 需要 sudo 密碼以存取檔案
    today = date.today()
    agent_pc_id = "000"
    agent_pi_id = "001"
    agent_pi_ip = "192.168.65.45:80"
    agent_pc_ip = '192.168.65.54'
    sudoPassword = 'uscc' # 0
    dir_path = '/home/ne6101157/wazuh_data'
    hidsdirpath = '/home/ne6101157/wazuh_data' #('放你的wazuhlog存放路徑 不包含年月日'+'/'+today.year+'/'+today.strftime("%b")+'/ossec-alerts-'+today.day+'.json')
    nidsdirpath = '/home/ne6101157/dashboard' #nids存放路徑 不包含檔名
    pcapdirpath = ''
    csvpath= '/home/ne6101157/dashboard/feature3.csv'
    modelpath = '/home/ne6101157/dashboard/pima.pickle.dat'
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
