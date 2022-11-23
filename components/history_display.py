# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output
# from dash import dcc, html, callback, dash_table

# import globals
# from plot import nbar
# from components.se_display import CONFIG

# global CONFIG

# BAR_STYLE = {'zIndex':1} #'border':'1px black solid', 

# def update(startDate, endDate, freqs, ip):
#     global CONFIG

#     # 若所選 fields 中沒有 timestamp, 則自動加入 timestamp 在最前面
#     if len(globals.n_selected_fields) != 0 and 'timestamp' not in globals.nselected_fields:
#         globals.n_selected_fields.insert(0, 'timestamp')

#     # 若 fields 中只剩下 timestamp=> 刪除 timestamp, 讓 fields 為空 (data table 會顯示所有 fields)
#     elif globals.n_selected_fields == ['timestamp']:
#         globals.n_selected_fields.remove('timestamp')

#     # 根據 selected_fields 篩選資料(若 fields 為空, table 顯示所有 fields)
#     global df
#     bar_fig, df = nbar.update(startDate, endDate, freqs, globals.n_selected_fields, ip)
#     # 若無資料
#     if len(df) == 0:
#         return [f'從 {startDate} 到 {endDate}', '此區間無資料', []]

#     # 若有資料
#     df.insert(0, '#', [i for i in range(1, len(df)+1)])
#     all_cols = list(df.columns)
#     bar_graph = dcc.Graph(
#         figure=bar_fig,
#         id='nbar_chart', clickData=None, hoverData=None,
#         config=CONFIG, style=BAR_STYLE,
#     )

#     # 解決 data table 中 list 的顯示問題, 將 df 中的 list 轉成 string 用逗號隔開, 並串接在一起
#     for column in all_cols:
#         df[column] = [', '.join(map(str, l)) if isinstance (l, list) else l for l in df[column]]

#     # 根據 column 名稱長度, 自動調整 data table 的 header 寬度
#     long_column_names = [{"if": {"column_id": column}, "min-width": "300px"} for column in all_cols if len(column) >= 30]
#     med_column_names = [{"if": {"column_id": column}, "min-width": "225px"} for column in all_cols if (len(column) > 15 and len(column)) < 30]
#     small_column_names = [{"if": {"column_id": column}, "min-width": "120px"} for column in all_cols if len(column) <= 15]

#     adjusted_columns = long_column_names + med_column_names + small_column_names

#     table = dash_table.DataTable(
#         data=df.to_dict('records'),
#         columns=[{'name': column, 'id': column} for column in all_cols],
#         virtualization=True,
#         sort_action='custom',
#         sort_mode='multi',
#         # 要 minWidth, maxWidth 同時設一樣, 再搭配 fixed_rows, 才能 fixed header
#         style_cell={
#             'textAlign': 'left',
#             'overflow': 'hidden',
#             'textOverflow': 'ellipsis',
#             'minWidth': 240,
#             'maxWidth': 240,
#             # 'whiteSpace': 'pre-line',   # 超過自動換行
#         },
#         fixed_rows={
#             'headers': True,
#             'data': 0,
#         },
#         style_cell_conditional=adjusted_columns,
#         # filter_action="native",
#         style_data_conditional=[
#             {
#                 'if': {'row_index': 'odd'},
#                 'backgroundColor': 'rgb(220, 248, 248)',
#             }
#         ],
#         style_header={
#             'backgroundColor': 'rgb(230, 230, 230)',
#             'color': 'black',
#             'fontWeight': 'bold',
#             'textAlign': 'left',
#             'border':'1px black solid',
#             'minWidth': '100%',
#         },
#         tooltip_data=[
#             {
#                 column: {'value': f'{value}', 'type': 'markdown'}
#                 for column, value in row.items()
#             } for row in df.to_dict('records')
#         ],
#         tooltip_header={i: i for i in all_cols},
#         id='hdash-table',
#         page_action='custom',   # 後端分頁
#         page_current=0,
#         page_size=100,
#         tooltip_delay=0,
#         tooltip_duration=None
#     )

#     default_page_size = 100 # 每頁預設 data 數
#     display = [
#         bar_graph,
#         html.Br(),
#         dbc.Row(
#             [
#                 html.H3(f'每頁{default_page_size}筆', style={'margin-left': '15px'}, id='hpage-size'),
#                 dcc.Dropdown(value=default_page_size, clearable=False, style={'width': '35%', 'margin-left': '15px'},
#                              options=[10, 25, 50, 100], id='hrow_drop')
#             ]
#         ),
#         table,
#     ]

#     return [f'從 {startDate} 到 {endDate}', f'{len(df)} hits', display]

# # 後端分頁, 以減少延遲和內存壓力, 外加排序功能
# @callback(
#     [
#         Output('hdash-table', 'data'),
#         Output('hdash-table', 'page_count'),
#         Output('hdash-table', 'tooltip_data'),
#         Output('hpage-size', 'children'),
#     ],
#     [
#         Input('hdash-table', 'page_current'),
#         Input('hdash-table', 'page_size'),
#         Input('hdash-table', 'sort_by'),
#         Input('hrow_drop', 'value'),
#     ]
# )
# def refresh_page_data(page_current, page_size, sort_by, value):
#     global df
#     page_size = value

#     # sort_by 紀錄參與排序的 col_name, 以及其排序方式(asc, desc)
#     if sort_by:
#         df = df.sort_values(
#             [col['column_id'] for col in sort_by],
#             ascending=[
#                 col['direction'] == 'asc'
#                 for col in sort_by
#             ]
#         )

#     return [
#         df.iloc[page_current * page_size:(page_current + 1) * page_size].to_dict('records'),
#         1 + df.shape[0] // page_size,
#         [
#             {
#                 column: {'value': f'{value}', 'type': 'markdown'}
#                 for column, value in row.items()
#             } for row in df.iloc[page_current * page_size:(page_current + 1) * page_size].to_dict('records')
#         ],
#         f'每頁{page_size}筆'
#     ]
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, html, callback, dash_table
import pandas as pd
import globals
from components.se_display import CONFIG
from components import nids_logtojson
from datetime import date
import datetime
import time
global CONFIG

BAR_STYLE = {'zIndex':1} #'border':'1px black solid', 

def update(startDate, endDate, freqs, ip):
    global CONFIG
    
    dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    starttime = datetime.datetime.strptime(startDate, dateFormat).strftime("%H:%M:%S")
    endtime = datetime.datetime.strptime(endDate, dateFormat).strftime("%H:%M:%S")
    startDate = datetime.datetime.strptime(startDate, dateFormat).strftime("%m-%d-%Y")
    endDate = datetime.datetime.strptime(endDate, dateFormat) .strftime("%m-%d-%Y")

    nids_logtojson.log2json(globals.nidsdirpath+"/fast.log")

    #讀取json檔, 篩選今天的log內容
    global df
    df = pd.read_json(globals.nidsdirpath+"/fast.json")
    # 若有資料
    df.insert(0, '#', [i for i in range(1, len(df)+1)])
    df['Date'] = pd.to_datetime(df['Date'])
    mask = (df['Date'] >=startDate) &(df['Date'] <= endDate)
    mask1 = (df['Time'] >=starttime) &(df['Time'] <= endtime)
    df = df.loc[mask]
    df = df.loc[mask1]
    all_cols = list(df.columns)
    print(all_cols)

    # # 解決 data table 中 list 的顯示問題, 將 df 中的 list 轉成 string 用逗號隔開, 並串接在一起
    # for column in all_cols:
    #     df[column] = [', '.join(map(str, l)) if isinstance (l, list) else l for l in df[column]]

    # 根據 column 名稱長度, 自動調整 data table 的 header 寬度
    long_column_names = [{"if": {"column_id": column}, "min-width": "300px"} for column in all_cols if len(column) >= 30]
    med_column_names = [{"if": {"column_id": column}, "min-width": "225px"} for column in all_cols if (len(column) > 15 and len(column)) < 30]
    small_column_names = [{"if": {"column_id": column}, "min-width": "120px"} for column in all_cols if len(column) <= 15]

    adjusted_columns = long_column_names + med_column_names + small_column_names

    table = dash_table.DataTable(
        id = 'hdash-table',
        data=df.to_dict('records'),
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in all_cols
        ],
        virtualization=True,
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        # 要 minWidth, maxWidth 同時設一樣, 再搭配 fixed_rows, 才能 fixed header
        style_cell={
            'textAlign': 'left',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'minWidth': 240,
            'maxWidth': 240,
            # 'whiteSpace': 'pre-line',   # 超過自動換行
        },
        fixed_rows={
            'headers': True,
            'data': 0,
        },
        style_cell_conditional=adjusted_columns,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 248, 248)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'left',
            'border':'1px black solid',
            'minWidth': '100%',
        },
    )

    display = [
        html.Br(),
        # dbc.Row(
        #     [
        #         html.H3(f'每頁{default_page_size}筆', style={'margin-left': '15px'}, id='hpage-size'),
        #         dcc.Dropdown(value=default_page_size, clearable=False, style={'width': '35%', 'margin-left': '15px'},
        #                      options=[10, 25, 50, 100], id='hrow_drop')
        #     ]
        # ),
        table,
    ]

    return [f'從 {startDate} 到 {endDate}', display]

@callback(
    Output('hdash-table', 'style_data_conditional'),
    Input('hdash-table', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]
