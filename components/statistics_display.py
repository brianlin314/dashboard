import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import datetime
from database import get_ndb
from components import nids_logtojson
import pandas as pd
import plotly.graph_objects as go
import globals

# set donut chart top num
class_topNum = 3
class_title = f'Top {class_topNum} class'
sip_topNum = 5
sip_title = f'Top {sip_topNum} source ip'
dip_topNum = 5
dip_title = f'Top {dip_topNum} destination ip'

CONFIG = {
    'staticPlot': False,     # True, False
    'scrollZoom': True,      # True, False
    'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
    'showTips': True,       # True, False
    'displayModeBar': True,  # True, False, 'hover'
    'watermark': False,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d','select2d'],
}

FIRST_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": 23,
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'width': '40%',
    'zIndex':1,
}


def update(startDate, endDate, freqs, ip):
    # get chart
    # alertdonut.update(startDate, endDate, ip)
    global CONFIG
    
    dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    starttime = datetime.datetime.strptime(startDate, dateFormat).strftime("%H:%M:%S")
    endtime = datetime.datetime.strptime(endDate, dateFormat).strftime("%H:%M:%S")
    startDate = datetime.datetime.strptime(startDate, dateFormat).strftime("%Y-%m-%d")
    endDate = datetime.datetime.strptime(endDate, dateFormat) .strftime("%Y-%m-%d")
    nids_logtojson.log2json(globals.nidsdirpath+"/fast.log")

    #讀取json檔, 篩選今天的log內容
    global df
    df = pd.read_json(globals.nidsdirpath+"/fast.json")
    # 若有資料
    df.insert(0, '#', [i for i in range(1, len(df)+1)])
    df['Date'] = pd.to_datetime(df['Date'])
    print(df['Time'].tail(3))
    mask = (df['Date'] >=startDate) &(df['Date'] <= endDate)
    # mask1 = (df['Time'] >=starttime) &(df['Time'] <= endtime)
    df = df.loc[mask]
    print(df.shape)

    df['Source'].value_counts()
    df['Destination'].value_counts()
    df['Protocol'].value_counts()
    df['Classification'].value_counts()

    total = df.shape[0]
    high = df[df['Priority']==1].shape[0]

    labels = list(df['Classification'].value_counts().head(class_topNum).index)
    values = list(df['Classification'].value_counts().head(class_topNum).values)
    class_fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    class_fig.update_layout(title_text=f"<b>{class_title}</b>")


    labels = list(df['Source'].value_counts().head(sip_topNum ).index)
    values = list(df['Source'].value_counts().head(sip_topNum ).values)
    sip_fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    sip_fig.update_layout(title_text=f"<b>{sip_title}</b>")

    labels = list(df['Destination'].value_counts().head(dip_topNum).index)
    values = list(df['Destination'].value_counts().head(dip_topNum).values)
    dip_fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    dip_fig.update_layout(title_text=f"<b>{dip_title}</b>")


    class_graph = dcc.Graph(
        figure=class_fig,
        clickData=None, hoverData=None,
        config=CONFIG, style=FIRST_STYLE,
    )
    sip_graph = dcc.Graph(
        figure=sip_fig,
        clickData=None, hoverData=None,
        config=CONFIG, style=FIRST_STYLE,
    )
    dip_graph = dcc.Graph(
        figure=dip_fig,
        clickData=None, hoverData=None,
        config=CONFIG, style=FIRST_STYLE,
    )
    first_row = [class_graph]
    second_row = [sip_graph, dip_graph]

    return [f'從 {startDate} 到 {endDate}', total, high, first_row, second_row]