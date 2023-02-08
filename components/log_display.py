import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, html, callback, dash_table
import pandas as pd
import json
from pandas import json_normalize
import globals
from datetime import date
from components import nids_logtojson
table_style = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "position":"relative",
    "left":"0.5rem",
    "top":"2rem",
    'fontsize':12,
}


# global CONFIG

def update(ip):
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    nids_logtojson.log2json(globals.nidsdirpath+"/fast.log")

    #讀取json檔, 篩選今天的log內容
    global df
    df = pd.read_json(globals.nidsdirpath+"/fast.json")
    mask = df['Destination'] == ip
    df1 = df.loc[mask]
    mask1 = df['Source'] == ip
    df2 = df.loc[mask1]
    df = pd.concat([df1,df2])
    mask1 =df['Date'] == today
    df = df.loc[mask1]
    df = df.loc[:, ["Date", "Time", "Signature Id", "Classification", "Priority", "Protocol", "Source", "Destination"]]
    df['Date'] = df['Date'].apply(lambda x: x.strftime("%Y/%m/%d"))
    df= df.sort_values(by='Time',ascending=False)
    all_cols = list(df.columns)
    table = dash_table.DataTable(
        virtualization=True,
        data=df.to_dict('records'),
        columns=[{'name': column, 'id': column} for column in all_cols],
        # fixed_columns={ 'headers': True, 'data': 1},
        style_header={
            'backgroundColor': '#99ABBD',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border':'1px black solid',
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell={
            # all three widths are needed
            'width': '180px',
            # 'overflow': 'hidden',
            # 'textOverflow': 'ellipsis',
            'textAlign': 'center',
            'fontsize':12,
            'height': 'auto',

        },
        style_table={
            'minWidth': '100%',
            'Width': '100%'
        },
    )

    # # default_page_size = 100 # 每頁預設 data 數
    # display = [
    #     html.Br(),
    #     table,
    # ],style = table_style

    return table
