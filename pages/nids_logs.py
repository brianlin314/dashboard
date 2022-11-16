import dash_bootstrap_components as dbc
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL
import feffery_antd_components as fac
import pandas as pd
from datetime import date
import globals
import dash
from components import log_display, nids_logtojson
# components
hitNum = html.H1(
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='dataNum'
)


dropdown_style = {
    "display":"inline-block",
    "fontSize":20,
    'width': '200px',
    "position":"relative",
    "left":"1rem",
    "top":"1rem",
    "bottom":"2rem"
}

STYLE = {
    "transition": "margin-left .5s",
    "margin-top": "2rem",
    "margin-left": "15rem",
    "margin-right": "0.5rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'zIndex':1,
    # 'border':'1px black solid',
    "position":"relative",
    "left":"0.5rem",
    "top":"1rem"

}

table_style = {
    "margin-right": "0.5rem",
    'width':'100%',
    'height':'500px',
    'minWidth': '100%',
    "position":"relative",
    "left":"0.5rem",
    "top":"2rem",
    
}


def serve_layout():
    layout = html.Div(
        [
            html.H4("Please Choose the Agent"),
            dbc.Row(
                fac.AntdSelect(
                    id = 'agentselect',
                    placeholder='Agent:',
                    options=[
                        {'label': 'Raspberry Pi', 'value': 'Raspberry Pi'},
                        {'label': 'PC', 'value': 'PC'},
                    ],
                    style=dropdown_style
                ),
            ),
            dbc.Row(
                html.Div(
                        id='table'
                ),style = table_style,
            )
        ],
        style=STYLE,
    )
    return layout

@callback(
    Output('table', 'children'),
    Input('agentselect', 'value'),
    prevent_initial_call=True
)

def update(value):
    if(value=='Raspberry Pi'):
        return log_display.update(globals.agent_pi_ip)
    elif(value=='PC'):
        return log_display.update(globals.agent_pc_ip)
    return dash.no_update