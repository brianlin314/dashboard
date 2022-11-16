import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, html, callback, dash_table
import pandas as pd
import json
from pandas import json_normalize
import globals
from datetime import date
from components import nids_logtojson
from usb_data import usb
import dash
import feffery_antd_components as fac

# global CONFIG

def update(id):
    usb.usbdf()
    # AUSB = 2
    # UUSB = 2
    # Total = 2
    #讀取json檔, 篩選今天的log內
    global df
    df = pd.read_json("/home/server/dash_brain/usb_data/usb_info.json")
    id = int(id)
    df = df[(df["agent_id"] == id)]
    try:
        df['In_Time'] = df['In_Time'].apply(lambda x: x.strftime("%H:%M:%S"))
        df['Out_Time'] = df['Out_Time'].apply(lambda x: x.strftime("%H:%M:%S"))
    except:
        print(id)
    AUSB = df[((df['authorized'] == 'white')&(df['connected'] == 1))].shape[0]
    UUSB = df[((df['authorized'] == 'black')&(df['connected'] == 1))].shape[0]
    Total=  df[(df['connected'] == 1)].shape[0]
    all_cols = list(df.columns)
    table = dash_table.DataTable(
        virtualization=True,
        data=df.to_dict('records'),
        columns=[{'name': column, 'id': column} for column in all_cols],
        fixed_rows={'headers': True},
        #page_action='none'
        style_header={
            'backgroundColor': '#99ABBD',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
            # 'border':'1px black solid',
        },
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{authorized} = "black"',
                'column_id': 'authorized'
            },
            'backgroundColor': '#FD4000',
            'color': 'white'
        },
        ],
        style_cell={
            # all three widths are needed
            'width': '180px',
            # 'overflow': 'hidden',
            # 'textOverflow': 'ellipsis',
            'textAlign': 'center',
            'fontsize':12,
            'height': 'auto',

        },
        style_table={"height":2000, "width":"1445px"},
    )
    return [AUSB, UUSB, Total, table]
