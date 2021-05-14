import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from dash.dependencies import Input, Output
import plotly.express as px
from data import *


def parse_date(date_time):
    if 'T' in date_time:
        date = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        date = '{dt.month}/{dt.day}/'.format(dt=date) + date.strftime('%y')
        return date
    else:
        date = datetime.strptime(date_time, "%Y-%m-%d")
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
country = "Canada"
df = confirmed_cases.createCountry(country).get_seven_day_average_df()
fig = px.line(df, x="Date", y='{} cases'.format(confirmed_cases.type))
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
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
                minimum_nights=14),

            dcc.Checklist(
                id="checkbox",
                options=[{'label': 'Enable 7 day averaging',
                          'value': 'YES'}],
                value=['YES'])],
            style={'width': '25%', 'float': 'left', 'display': 'inline-block'}),
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
            style={'width': '25%', 'float': 'right', 'display': 'inline-block'}),
        html.Br(),
        html.H3(id='title',
                children=
                "Seven day average for confirmed cases in {}"
                .format(country),
                style={'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(id='plot', figure=fig),
        html.Br(),
        html.Br(),
        dcc.Markdown(
            '''## Usage 
#### Date range :
* Select the date range you are interested in.
* The earliest possible date is Jan 29th 2020.
* There must be a 14 day gap between the start and end dates
* If the calender stops you from selecting a date, that your selection is invalid.
 #### 7-day averaging:
* If you enable 7 day averaging, then the value on the y axis becomes the average for the prceeeding 7 days instesd of single day.
* #### Country:
* Select your country of interest using the drop down list. 
* #### Dataset:
* You can choose one of the three possible datasets (Confirmed, Deaths, Recovered).
* Note that since some countries do not rack recoveries the plot my not be accurate.
'''
            ,
            style={'textAlign': 'center', 'color': colors['text'],
                   'font-size': 18}
        )])


@app.callback(
    Output("plot", "figure"),
    Output('title', 'children'),
    Input("dataset-type", "value"),
    Input("country-value", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
    Input("checkbox", "value"))
def update_figure(dataset_type, country_value, start_date, end_date, checkbox):
    if dataset_type is None or dataset_type == "Confirmed":
        dataset = confirmed_cases
    elif dataset_type == "Recovered":
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
        figure_title = "Seven day average for {} cases in {}" \
            .format(dataset.type.lower(), country_value)
    else:
        updated_df = dataset.createCountry(country_value).get_record_df()
        figure_title = "Daily {} cases in {}" \
            .format(dataset.type.lower(), country_value)
    updated_df = updated_df.loc[min_date_i:max_date_i]
    figure = px.line(updated_df, x="Date", y='{} cases'.format(dataset.type))
    figure.update_layout(transition_duration=100)
    return figure, figure_title


if __name__ == '__main__':
    app.run_server()
