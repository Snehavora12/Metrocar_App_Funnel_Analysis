import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

df = pd.read_csv('user_base.csv')
# Link to user_base.csv : https://drive.google.com/file/d/1lL3XY7KEEZgMq6S9pFNQr6GC8Hs1ErzT/view?usp=sharing
df1 = pd.read_csv('ride_base.csv')
# Link to ride_base.csv : https://drive.google.com/file/d/1fc5bXEab-Hox9n5xzDJcb_NrsDIZFFuI/view?usp=sharing

user_funnel_steps = ['has_downloaded', 'has_signed_up', 'has_requested', 'has_accepted', 'has_completed', 'has_paid', 'has_reviewed']
rides_funnel_steps = ['has_requested', 'has_accepted', 'has_completed', 'has_paid', 'has_reviewed']

by_user = df.groupby('app_download_key')[user_funnel_steps].any().sum()
user_fig = px.funnel(by_user)

by_rides = df1.groupby('ride_id')[rides_funnel_steps].any().sum()
rides_fig = px.funnel(by_rides)
rides_fig.update_traces(textposition='inside',textinfo="value+percent previous")


app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    children=[
        html.H1(children="Metrocar Funnel Analysis"),
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='User Funnel (shows % of previous)', value='tab-1'),
            dcc.Tab(label='Rides Funnel (shows % of previous)', value='tab-2'),
        ]),
        html.Div(id='tabs-content')
    ]
)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Dropdown(id='user-dropdown',
                         value='app_download_key',
                         options=[
                             {'label': 'Age', 'value': 'age_range'},
                             {'label': 'Platform', 'value': 'platform'},
                             {'label': 'Users', 'value': 'app_download_key'}
                         ]),
            dcc.Graph(id="user-funnel-plot", figure=user_fig)
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(id="rides-funnel-plot", figure=rides_fig)
        ])

@app.callback(
    Output('user-funnel-plot', 'figure'),
    [Input('user-dropdown', 'value')]
)
def update_user_figure(selector):
    if selector == 'app_download_key':
        by_user = df.groupby(selector)[user_funnel_steps].any().sum()
        fig = px.funnel(by_user)
        fig.update_traces(textposition='inside', textinfo="value+percent previous")
    else:
        by_user = df.groupby(selector)[user_funnel_steps].sum().T

        fig = px.funnel(by_user)


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)