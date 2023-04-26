from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import date, timedelta

date_calendar = html.Div(
    [
        dbc.Label("Dates"),
        html.Br(),
        dcc.DatePickerRange(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 3, 31),
            max_date_allowed=(date.today()-timedelta(days=1)),
            min_date_allowed=date(1990, 1, 1),
            id='date_range'
        )
    ],
    style={'textAlign': 'center'}
)