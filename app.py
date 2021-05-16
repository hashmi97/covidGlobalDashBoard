import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from dash.dependencies import Input, Output
import plotly.express as px
from data import *


def parse_date(date_time):
    date = datetime.fromisoformat(date_time)
    date = '{dt.month}/{dt.day}/'.format(dt=date) + date.strftime('%y')
    return date


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    'background': '#ffffff',
    'text': '#000080'
}
confirmed_cases = Dataset(CONFIRMED)
death_cases = Dataset(DEATHS)
recovery_cases = Dataset(RECOVERED)
country = 'Canada'
df = confirmed_cases.createCountry(country).get_seven_day_average_df()
fig = px.line(df, x='Date', y='{} cases'.format(confirmed_cases.type))
available_countries = np.unique(confirmed_cases.countries)
available_dates = confirmed_cases.dates
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(children='COVID19-Dashboard',
                style={'textAlign': 'center',
                       'color': colors['text']}),
        html.Br(),
        html.Div([
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=datetime.strptime(available_dates[7],
                                                   '%m/%d/%y'),
                max_date_allowed=datetime.strptime(available_dates[-1],
                                                   '%m/%d/%y'),
                with_portal=True,
                end_date=datetime.strptime(available_dates[-1],
                                           '%m/%d/%y'),
                start_date=datetime(2021, 1, 1),
                start_date_placeholder_text='Start Period',
                end_date_placeholder_text='End Period',
                minimum_nights=14),

            dcc.Checklist(
                id='checkbox',
                options=[{'label': 'Enable 7 day averaging',
                          'value': 'YES'}],
                value=['YES'])],
            style={'width': '25%', 'float': 'left',
                   'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='country-value',
                options=[{'label': i, 'value': i} for i in
                         available_countries],
                value='Afghanistan'),
            dcc.RadioItems(
                id='dataset-type',
                options=[{'label': i, 'value': i} for i in
                         ['Confirmed', 'Deaths', 'Recovered']],
                value='Confirmed',
                labelStyle={'display': 'inline-block'}
            )],
            style={'width': '25%', 'float': 'right',
                   'display': 'inline-block'}),
        html.Br(),
        html.H3(id='title',
                children='Seven day average for confirmed cases in {}'
                .format(country),
                style={'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(id='plot', figure=fig),
        html.Br(),
        html.Div(children=['Copyright (C) 2021 Hisham Al Hashmi',
                           html.A('Github repo',
                                  href='https://github.com/hashmi97/'
                                       'covidGlobalDashBoard',
                                  target='_blank',
                                  style={'margin-left': '15px',
                                         'margin-right': '15px'}),
                           'The Data is copyrighted by Johns Hopkins '
                           'University 2020'
                           ], style={'width': '100%',
                                     'display': 'flex',
                                     'align-items': 'center',
                                     'justify-content': 'center',
                                     'textAlign': 'center'
                                     })
    ])


@app.callback(
    Output('plot', 'figure'),
    Output('title', 'children'),
    Input('dataset-type', 'value'),
    Input('country-value', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('checkbox', 'value'))
def update_figure(dataset_type, country_value, start_date, end_date, checkbox):
    if dataset_type is None or dataset_type == 'Confirmed':
        dataset = confirmed_cases
    elif dataset_type == 'Recovered':
        dataset = recovery_cases
    else:
        dataset = death_cases
    start_date_str = parse_date(start_date)
    end_date_str = parse_date(end_date)
    min_date_i = np.where(dataset.dates == start_date_str)[0][0]
    max_date_i = np.where(dataset.dates == end_date_str)[0][0]
    if len(checkbox) == 1:
        updated_df = dataset.createCountry(country_value) \
            .get_seven_day_average_df()
        figure_title = 'Seven day average for {} cases in {}' \
            .format(dataset.type.lower(), country_value)
        min_date_i -= 7
    else:
        updated_df = dataset.createCountry(country_value).get_record_df()
        figure_title = 'Daily {} cases in {}' \
            .format(dataset.type.lower(), country_value)
    updated_df = updated_df.loc[min_date_i:max_date_i]
    figure = px.line(updated_df, x='Date', y='{} cases'.format(dataset.type))
    figure.update_layout(transition_duration=100)
    return figure, figure_title


if __name__ == '__main__':
    app.run_server(debug=True)
