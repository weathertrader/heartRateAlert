
import os
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash()
colors = {
    'background': '#111111',
    'text': 'white'
    #'text': '#7FDBFF'
}
width_line  = 4
size_marker = 12
plot_height = 300
plot_width  = 800



def open_connection_to_db():
    print('open_connection_to_db ')    
    try:
         conn  = psycopg2.connect(database = os.environ['db_name'], 
                                  host     = os.environ['db_host'], 
                                  user     = os.environ['db_user_name'], 
                                  password = os.environ['db_password'], 
                                  port     = os.environ['db_port'])    
         autocommit = True
         if (autocommit):
             conn.autocommit = True
         cursor = conn.cursor()
         print      ('open_connection_to_db success ') 
    except:
        print      ('open_connection_to_db: ERROR ') 
    return conn, cursor

def get_most_recent_values_by_single_userid(conn,cursor,userid):
    #sql_statement = """SELECT userid, dt_last, lon_last, lat_last, total_dist FROM leaderboard WHERE userid = '%s'""" % (userid)
    sql_statement = """SELECT userid, dt_last, total_dist \
        FROM checkpoints WHERE userid = '%s' \
        ORDER BY dt_last DESC \
        LIMIT 1""" % (int(userid))
    # n = 33753
    # sql_statement = """SELECT userid, dt_last, lon_last, lat_last, total_dist FROM leaderboard WHERE userid = '%s'""" % (n)
    # cursor.execute(sql_statement)
    # results = cursor.fetchall()
    # print(results)
    #sql_statement = """SELECT userid, dt_last, lon_last, lat_last, total_dist 
    #                           FROM leaderboard 
    #                           ORDER BY total_dist DESC
    #                           LIMIT 10"""
    cursor.execute(sql_statement)
    user_most_recent_checkpoint = cursor.fetchall()[0]
    #print(leaders_df.head())
    return user_most_recent_checkpoint

def get_checkpoints_by_single_userid(conn,cursor,userid):
    sql_statement = """SELECT userid, dt_last, segment_dist, total_dist FROM checkpoints WHERE userid = '%s'""" % (int(userid))
    user_checkpoint_df = pd.read_sql(sql_statement,conn)
    #print(user_checkpoint_df.head())
    #user_last_checkpoint = user_checkpoint_df.iloc[0]['userid']
    #if (batch_df['id'][n] == 1):
    #    print('    found checkpoint user %s dt %5.1f lon %5.1f lat %5.1f  segment_dist %5.1f ' %(user_checkpoint_df.iloc[-1]['userid'], user_checkpoint_df.iloc[-1]['dt_last'], user_checkpoint_df.iloc[-1]['lon_last'], user_checkpoint_df.iloc[-1]['lat_last'], user_checkpoint_df.iloc[-1]['segment_dist']))
    return user_checkpoint_df

def get_current_leaderboard(conn,cursor):
    sql_statement = """SELECT userid, dt_last, segment_dist, total_dist \
        FROM checkpoints \
        WHERE total_dist IS NOT NULL \
        AND segment_dist < 2.0 \
        ORDER BY total_dist DESC \
        LIMIT 20""" 
    leaderboard_df = pd.read_sql(sql_statement,conn)
    print('leaderboard_df before dropping')
    print(leaderboard_df.head(20))
    leaderboard_df.drop_duplicates(subset='userid', keep='first', inplace=True)
    #print('leaderboard_df after dropping1')
    #print(leaderboard_df.head(20))
    leaderboard_df.reset_index(drop=True, inplace=True)
    #print('leaderboard_df after dropping1')
    #print(leaderboard_df.head(20))
    leaderboard_df = leaderboard_df.head(10)    
    #leaderboard_df.drop('segment_dist', axis=1, inplace=True)
    #leaderboard_df['userid'] = leaderboard_df['userid'].map("{:,.0f}".format)
    leaderboard_df['userid']  = leaderboard_df['userid'].map("{:.0f}".format)
    leaderboard_df['dt_last'] = leaderboard_df['dt_last'].map("{:.1f}".format)
    leaderboard_df['segment_dist'] = leaderboard_df['segment_dist'].map("{:.2f}".format)
    leaderboard_df['total_dist'] = leaderboard_df['total_dist'].map("{:.2f}".format)
    #leaderboard_df.head(50)
    return leaderboard_df

(conn,cursor) = open_connection_to_db()
(leaderboard_df) = get_current_leaderboard(conn,cursor)
#leaderboard_df.columns = ['userid', 'last reported time', 'distance_traveled']
leaderboard_df.columns = ['userid', 'last report [min]', 'last segment distance [km]', 'total distance [km]']
#print(leaderboard_df.head(10))
userid = leaderboard_df['userid'][0]
(user_checkpoint_df) = get_checkpoints_by_single_userid(conn,cursor,userid)
#print(user_checkpoint_df.head(20))


#(user_most_recent_checkpoint) = get_most_recent_values_by_single_userid(conn,cursor,userid)
#print(user_most_recent_checkpoint)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(html.H1('RaceCast'), style={'textAlign': 'center','color': colors['text']}),
    html.Div([        
        html.Div([
            html.Div(html.H2('Live Race Leaderboard'), style={'textAlign': 'center','color': colors['text']}),
            #html.Div(generate_table(leaderboard_df), style={'backgroundColor': 'white', 'color': 'black', 'margin-left': '20px', 'width': '100%', 'display': 'flex', 'align-items': 'right', 'justify-content': 'center'}),
            html.Div(id='div_table', style={'backgroundColor': 'white', 'color': 'black', 'margin-left': '20px', 'width': '100%', 'display': 'flex', 'align-items': 'right', 'justify-content': 'center'}),
            #html.Div(html.H2('Athlete Tracker,  Enter ID'), style={'color': colors['text'],'margin-top': '10px', 'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),       
            #html.Div(html.H2(id='div_display-userid', style={'textAlign': 'center','color': colors['text']})),
            
            html.Div([
                #dcc.Input(id='div_user_id_text_box', value='41',type='text', style={'color': 'black', 'margin-left': '20px', 'margin-right': '20px'}), 
                dcc.Input(id='div_user_id_text_box', value=userid, type='text', style={'color': 'black', 'margin-left': '20px', 'margin-right': '20px'}), 
                html.Button('Submit', id='submit-val', n_clicks=0, style={'color': colors['text']})
            ], style={'color': colors['text'],'margin-top': '50px','margin-bottom': '20px', 'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}, className="row"),
        ], className="six columns"),
        html.Div([
            html.Div(html.H2('Leaderboard Checkpoints'), style={'textAlign': 'center','color': colors['text']}),
            #html.Div(html.H2('Leaderboard Progress vs Time'), style={'margin-top': '10px', 'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
            html.Div(id='div_figure1', style={'margin-top': '20px', 'width': '100%', 'align-items': 'center', 'justify-content': 'center'}),       
            #html.Div(html.H2('User Progress vs Time'), style={'margin-top': '10px', 'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
            html.Div(html.H2(id='div_display-userid', style={'color': colors['text'],'margin-top': '20px', 'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})),
            html.Div(id='div_figure2', style={'margin-top': '20px','margin-bottom': '20px', 'width': '100%', 'align-items': 'center', 'justify-content': 'center'}),       
        ], className="six columns"),
    ], className="row")
])


@app.callback(
    dash.dependencies.Output('div_table', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('div_user_id_text_box', 'value')])
def generate_table(n_clicks,input_value):
    (leaderboard_df) = get_current_leaderboard(conn, cursor)        
    #leaderboard_df
    max_rows=20
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in leaderboard_df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(leaderboard_df.iloc[i][col]) for col in leaderboard_df.columns
            ]) for i in range(min(len(leaderboard_df), max_rows))
        ])
    ])



@app.callback(
    dash.dependencies.Output('div_display-userid', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('div_user_id_text_box', 'value')])
def update_output_div(n_clicks,input_value):
    (results) = get_most_recent_values_by_single_userid(conn,cursor,input_value)
    #print(results)
    text = 'User '+str(results[0])+ ' total distance '+str("{:.1f}".format(results[2]))+ ' km as of '+str("{:.1f}".format(results[1]))+' min'
    #print(text)
    #return 'User selected is {}'.format(input_value)
    return text

@app.callback(
    dash.dependencies.Output('div_figure1', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('div_user_id_text_box', 'value')])
def update_graph1(n_clicks, div_user_id_text_box):
    (leaderboard_df) = get_current_leaderboard(conn, cursor)
    #print(leaderboard_df.head(20))    
    leaders_ids = leaderboard_df['userid']
    #print(leaders_ids)
    n_leaders = len(leaders_ids)
    #print ('found %s leaders' %(n_leaders))
    x_max = 0.0
    y_max = 0.0
    #for n in range(0, n_leaders, 1):
    for n in range(0, 5, 1):
        #print ('  processing leader %s with id %s ' %(n, leaders_ids[n]))
        (user_checkpoint_df) = get_checkpoints_by_single_userid(conn,cursor,leaders_ids[n])
        #print(user_checkpoint_df)
        x_max = max(x_max, np.nanmax(user_checkpoint_df['dt_last']))
        y_max = max(y_max, np.nanmax(user_checkpoint_df['total_dist']))
        #print(user_checkpoint_df.head(20))
        if   (n == 0):
            df_temp0 = user_checkpoint_df
        elif (n == 1):
            df_temp1 = user_checkpoint_df
        elif (n == 2):
            df_temp2 = user_checkpoint_df
        elif (n == 3):
            df_temp3 = user_checkpoint_df
        elif (n == 4):
            df_temp4 = user_checkpoint_df
        #print ('  done processing  ')

    # dash='dash', dash='dot'
    x_max = x_max+1
    y_max = y_max+1
    return dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=df_temp0['dt_last'],
                    y=df_temp0['total_dist'],
                    name=leaders_ids[0],
                    marker=dict(color='red', size=size_marker),
                    line  =dict(color='red', width=width_line)),
                dict(
                    x=df_temp1['dt_last'],
                    y=df_temp1['total_dist'],
                    name=leaders_ids[1],
                    marker=dict(color='blue', size=size_marker),
                    line  =dict(color='blue', width=width_line)),
                dict(
                    x=df_temp2['dt_last'],
                    y=df_temp2['total_dist'],
                    name=leaders_ids[2],
                    marker=dict(color='green', size=size_marker),
                    line  =dict(color='green', width=width_line)),
                dict(
                    x=df_temp3['dt_last'],
                    y=df_temp3['total_dist'],
                    name=leaders_ids[3],
                    marker=dict(color='magenta', size=size_marker),
                    line  =dict(color='magenta', width=width_line)),
                dict(
                    x=df_temp4['dt_last'],
                    y=df_temp4['total_dist'],
                    name=leaders_ids[4],
                    marker=dict(color='cyan', size=size_marker),
                    line  =dict(color='cyan', width=width_line)),
            ],
            layout=dict(
                #title='Leaderboard Checkpoints',
                xaxis={'title': 'elapsed time [min]',
                       'type': 'linear',
                       'range': [0, x_max],
                       'size': 16,
                       'font': dict(size=30)
                      },
                yaxis={'title': 'distance traveled [km]',
                       'type': 'linear', 
                       'range': [0, y_max],
                       'font' : 30,
                      },
                showlegend=True,
                legend=dict(x=0.0,y=1.0, font_size=16),                
                margin=dict(autoexpand=False,l=80, r=60, t=60, b=60, pad=4),
                paper_bgcolor='white',
            )
        ),
        style={'height': plot_height, 'width': plot_width},
    )


n_clicks = 10
@app.callback(
    dash.dependencies.Output('div_figure2', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('div_user_id_text_box', 'value')])
def update_graph2(n_clicks, div_user_id_text_box):
    (user_checkpoint_df) = get_checkpoints_by_single_userid(conn,cursor,div_user_id_text_box)
    x_max = np.nanmax(user_checkpoint_df['dt_last'])+1
    y_max = np.nanmax(user_checkpoint_df['total_dist'])+1
    #print(user_checkpoint_df.head())
    return dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=user_checkpoint_df['dt_last'],
                    y=user_checkpoint_df['total_dist'],
                    name=div_user_id_text_box,
                    marker=dict(color='red', size=size_marker),
                    line  =dict(color='red', width=width_line)),
            ],
            layout=dict(
                #title='User '+str(div_user_id_text_box)+' Checkpoints',
                xaxis={'title': 'elapsed time [min]',
                       'type': 'linear',
                       'range': [0, x_max]
                      },
                yaxis={'title': 'distance traveled [km]',
                       'type': 'linear', 
                       'range': [0, y_max]
                      },
                #x='x Axis Title',
                #xaxis=dict('title':'title_text',  range:(0,10,1)),
                #y='y Axis Title',
                #yaxis={'range': range(0,10,1)},
                showlegend=True,
                legend=dict(x=0,y=1.0),
                #margin=dict(autoexpand=True, pad=40),
                #margin=dict(autoexpand=False,l=100, r=20, t=100, b=20, pad=4),
                margin=dict(autoexpand=False,l=80, r=60, t=60, b=60, pad=4),
                paper_bgcolor='white',                
                )    
            ),
        style={'height': plot_height, 'width': plot_width},
    )

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True, port=8050, host='ec2-34-222-54-126.us-west-2.compute.amazonaws.com')



######################################
# auto refresh 

#dcc.Interval(
#    id='interval-component',
#    interval=1*1000, # in milliseconds
#    n_interval=0)
# app.layout = html.Div(
#     [
#     html.H4('Stock_Data_Streaming'),
#     dcc.Graph(id='live-graph', animate=True), 
#     dcc.Interval(
#         id='graph-update',
#         interval=1*100,
#         n_intervals=0
#     )
#     ]
# )
#app.layout = html.Div(
#    html.Div([
#        html.H4('TERRA Satellite Live Feed'),
#        html.Div(id='live-update-text'),
#        dcc.Graph(id='live-update-graph'),
#        dcc.Interval(
#            id='interval-component',
#            interval=1*1000, # in milliseconds
#            n_intervals=0
#        )
#    ])
#)

# auto refresh 
######################################
