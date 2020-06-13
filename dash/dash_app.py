
import os
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    

    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                       350, 430, 474, 526, 488, 537, 500, 439],
                    name='Rest of world',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                       299, 340, 403, 549, 499],
                    name='China',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='US Export of Plastic Scrap',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    ) 
])




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

def get_leaders_from_db(conn,cursor):
    # sql_statement = """SELECT userid, dt, lon_last, lat_last, total_dist FROM leaderboard WHERE userid = '%s'""" % (n)
    # sql_statement = """SELECT userid, dt, lon_last, lat_last, total_dist 
    sql_statement = """SELECT userid, dt, total_dist 
                               FROM leaderboard 
                               ORDER BY total_dist DESC
                               LIMIT 10"""
    leaders_df = pd.read_sql(sql_statement,conn)
    #cursor.execute(sql_statement)
    #results = cursor.fetchall()
    print(leaders_df.head())
    return leaders_df

def get_values_by_userid(conn,cursor,userid):
    #sql_statement = """SELECT userid, dt, lon_last, lat_last, total_dist FROM leaderboard WHERE userid = '%s'""" % (userid)
    sql_statement = """SELECT userid, dt, total_dist FROM leaderboard WHERE userid = '%s'""" % (userid)
    # n = 33753
    # sql_statement = """SELECT userid, dt, lon_last, lat_last, total_dist FROM leaderboard WHERE userid = '%s'""" % (n)
    # cursor.execute(sql_statement)
    # results = cursor.fetchall()
    # print(results)
    #sql_statement = """SELECT userid, dt, lon_last, lat_last, total_dist 
    #                           FROM leaderboard 
    #                           ORDER BY total_dist DESC
    #                           LIMIT 10"""
    #leaders_df = pd.read_sql(sql_statement,conn)
    cursor.execute(sql_statement)
    results = cursor.fetchall()
    #print(leaders_df.head())
    return results

def generate_table(leaders_df, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in leaders_df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(leaders_df.iloc[i][col]) for col in leaders_df.columns
            ]) for i in range(min(len(leaders_df), max_rows))
        ])
    ])

(conn,cursor) = open_connection_to_db()
leaders_df = get_leaders_from_db(conn, cursor)
leaders_df.columns = ['userid', 'last reported time', 'distance_traveled']
leaders_df.head()


userid = 33753
(results) = get_values_by_userid(conn,cursor,userid)
print(results)


#    html.H1(children='RaceCast: Live Race Leaderboard'),
#app.layout = html.Div(children=[
app.layout = html.Div([
    html.H1('RaceCast: Live Race Leaderboard'),
    generate_table(leaders_df),
    html.Label('Enter Athlete ID'),
    dcc.Input(id='user_id_text_box', value='9324', type='text'),
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
    #dcc.Graph(id='graph1')
])

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

#    Output(component_id='my-div', component_property='children'),
#    [Input(component_id='my-id',  component_property='value')]


@app.callback(
    Output('my-div', 'children'),
    [Input('my-id',  'value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)

#@app.callback(
#    [Output('graph1', 'figure')],
#    [Input('user_id_text_box', 'value')
#    ]
#)

#@app.callback(
#    [Output(component_id='graph1', component_property='figure')],
#    [Input (component_id='user_id_text_box', component_property='value')])

#@app.callback(
#    Output('barplot-topactivity', 'figure'),
#    [Input('activity', 'value'),
#    Input('slider_updatetime', 'value')])
#def update_graph(activity, slider_updatetime):


#@app.callback(
#     Output('graph1', 'figure'),
#     [Input('user_id_text_box', 'value')
#     ]
# )

# def update_graph(user_id_text_box):
#     (results) = get_values_by_userid(conn,cursor,userid)
#     print(results)
#     cursor = connection.cursor()
#     table_name = activity + 'event_table'
#     start_time = getSliderTime(slider_updatetime)
#     y_label = "label"
#     if activity == 'aggregate':
#         y_label = "aggregate score"
#         cursor.execute("select repo_name, sum(score)  from {} where create_date >= \'{}\' group by repo_name ORDER BY sum(score) desc LIMIT 20".format(table_name, start_time))
#     else:
#         y_label = "no. of " + activity.lower() + " events"
#         y_label = "no. of " + activity.lower() + " events"
#         cursor.execute("select repo_name, sum(count)  from {} where create_date >= \'{}\' group by repo_name ORDER BY sum(count) desc LIMIT 20".format(table_name, start_time))
#     data = cursor.fetchall()
#     repo_list = []
#     count_list = []
#     for i in range(len(data)):
#         repo_list.append(data[i][0])
#         count_list.append(data[i][1])
#     return {
#         'data': [go.Bar(
#             x=repo_list,
#             y=count_list,
#             opacity= 0.5,
#             marker={'color':'#800080'}
#         )],
#         'layout': go.Layout(
#             yaxis={'title': '{}'.format(y_label)},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest',
#             plot_bgcolor='rgb(240,248,255)'
#         )
#     }




#''' This functions converts a dataframe into an HTML table '''
# def generate_table2(leaders_df, max_rows=10):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in leaders_df.columns])] +

#         # Body
#         [html.Tr([
#             html.Td(html.A(str(int(leaders_df.iloc[i][col])), href='https://stackoverflow.com/questions/'+str(int(leaders_df.iloc[i][col])))) for col in leaders_df.columns
#         ]) for i in range(min(len(leaders_df), max_rows))]
#     )






# top_tags = ['java','python','scala','javascript','c','git'] # top 7 tags to be chosen as input

# app.layout = html.Div([
# 	
# 	# This div contains the header
# 	html.Div([ html.H1(children='Spam Stack')
#                ], className= 'twelve columns', style={'textAlign':'center'}) ,

# 	# This div contains a dropdown to record the user input
#     html.Div([ dcc.Dropdown( id = 'input-tag',
#                              options = [{ 'label': val , 'value': val} for val in top_tags],
#                              value='java')

#     ]),

#     # This div contains a scatter plot which comapres the scores of posts and the table with posts that need most cleaning
#     html.Div([
#             html.Div([dcc.Graph(id='g1')],className='ten columns'),
#             html.Div([html.Div(id='table-container',)] 
#              , className='two columns'),
            
#     ]),

# ])

# @app.callback(
#     [Output(component_id='g1', component_property='figure'),
#     Output(component_id='table-container', component_property='children')],
#     [Input(component_id='input-tag', component_property='value')])
    
# def make_query(input_tag):
#     custom_query_1 = " SELECT  *  from " + input_tag + "_avg_score order by "+ input_tag +"_avg_score.\"_ParentId\"  LIMIT 1000; "
#     df1 = load_data(custom_query_1)
#     custom_query_2 = " SELECT * from " + input_tag + "_avg_new LIMIT 1000;"
#     df2 = load_data(custom_query_2)
#     custom_query_3 = " SELECT "+ input_tag +"_improv.\"_ParentId\" as \"Posts\" from " + input_tag + "_improv LIMIT 7;"
#     df3 = load_data(custom_query_3)
#     data_table = generate_table(df3)
#     return [{'data': [{'x': df1['_ParentId'], 'y': df1['_avgscore'],'mode':'markers', 'name':'Before'},
#                       {'x': df2['_ParentId'], 'y': df2['_avgscore'],'mode':'markers','opacity':0.7,'name':'After'}],
#          	'layout': {'xaxis': {'title': 'Post Id'}, 'yaxis': {'title': 'Score'}}},
#          	data_table]
 
# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

# app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
#     html.H1(
#         children='Hello Dash',
#         style={
#             'textAlign': 'center',
#             'color': colors['text']
#         }
#     ),

#     html.Div(children='Dash: A web application framework for Python.', style={
#         'textAlign': 'center',
#         'color': colors['text']
#     }),

#     dcc.Graph(
#         id='example-graph-2',
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#             ],
#             'layout': {
#                 'plot_bgcolor': colors['background'],
#                 'paper_bgcolor': colors['background'],
#                 'font': {
#                     'color': colors['text']
#                 }
#             }
#         }
#     )
# ])


#if __name__ == '__main__':
#    app.run_server(debug=True,host="0.0.0.0",port=80)

    
    