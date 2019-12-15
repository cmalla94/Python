# the budget manager page

# necessary imports
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import datetime as dt
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table as dtbl
import dash_table.FormatTemplate as FormatTemplate


# import the app
from app import app

# available categories
cat = ['Food', 'Gifts', 'Health', 'Home', 'Transportation', 'Personal', 'Subscriptions', 'Entertainment']

# available cities
cities = pd.read_csv('data_cleaned.csv')
cities = cities.City.unique()

# today's date
today = dt.date.today()

# read data
df = pd.read_csv('transactions.csv')

# add new transactions modal
def modal():
    return html.Div(
        html.Div(
            [
                html.Div(
                    [   

                        # modal header
                        html.Div(
                            [
                                html.Span(
                                    "New Transaction",
                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                html.Span(
                                    "×",
                                    id="modal_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # modal form
                        html.Div(
                            [
                                html.P(
                                    [
                                        "Category",
                                        
                                    ],
                                    style={
                                        "float": "left",
                                        "marginTop": "4",
                                        "marginBottom": "2",
                                    },
                                    className="row",
                                ),
                                dcc.Dropdown(
                                    id="category",
                                    options=[{'label': i, 'value': i} for i in cat],
                                    value="Food",
                                    clearable=False,
                                ),
                                html.P(
                                    "Purchase City",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="city",
                                    options=[
                                        {"label": city, "value": city}
                                        for city in cities
                                    ],
                                    value="New Westminster",
                                ),
                                html.P(
                                    "Purchase Place",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Input(
                                    id="place",
                                    placeholder='Enter place of purchase',
                                    type='text',
                                    value='',
                                ),
                                html.P(
                                    "Date",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.DatePickerSingle(
                                    id='purchase-date',
                                    date=dt.datetime(today.year, today.month, today.day)
                                ),
                                html.P(
                                    "Amount",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Input(
                                    id="amount",
                                    placeholder='Enter purchase amount',
                                    type='text',
                                    value='',
                                ),
                            ],
                            className="row",
                            style={"padding": "2% 8%"},
                        ),

                        # submit button
                        html.Span(
                            "Submit",
                            id="submit-btn",
                            n_clicks=0,
                            className="button button--primary add"
                        ),
                    ],
                    className="modal-content",
                    style={"textAlign": "center"},
                )
            ],
            className="modal",
        ),
        id="trans_modal",
        style={"display": "none"},
)

# page layout
layout = [
    html.Div(
            html.Span(
                "Add new",
                id="add-new-btn",
                n_clicks=0,
                className="button button--primary",
                style={
                    "height": "34",
                    "background": "#119DFF",
                    "border": "1px solid #119DFF",
                    "color": "white",
                },
            ),
        className="row",
        style={"marginBottom": "10"},
    ),
    modal(),
    html.Div( 
        dtbl.DataTable(
            id='trans-df',
            columns=[
                {
                    'id': 'amount',
                    'name': 'Price ($)',
                    'type': 'numeric',
                    'format': FormatTemplate.money(2)
                },
                {
                    'id': 'Date', 
                    'name': 'Date'
                },
                {
                    'id': 'Place',
                    'name': 'Place'
                },
                {
                    'id': 'City',
                    'name': 'City'
                },
                {
                    'id': 'Category',
                    'name': 'Category'
                }
            ],
            data=df.to_dict('records'),
            sorting=True,
            style_cell={
                'minWidth': '0px',
                'maxWidth': '120px',
                'whitespace': 'normal',
            },
            style_table={
                'height': '300px',
                'overflowX': 'scroll',
                'border': 'thin lightgrey solid',
                'backgroundColor': '#EDECDE'
            },
            n_fixed_rows=1,
            style_as_list_view=True,
            style_cell_conditional = [
                {
                    'if': {'column_id': i},
                    'textAlign': 'left'
                } for i in ['Date', 'amount', 'Place']
            ] + 
            [
                {
                    'if': {
                            'column_id': 'amount',
                        },
                    'backgroundColor': '#EF5939',
                    'width': '80px'
                }
            ] +
            [
                {
                    'if': {
                        'column_id': 'Date',
                    },
                    'width': '90px'
                }
            ] +
            [
                {
                    'if': {
                        'column_id': 'City',
                    },
                    'width': '120px'
                }
            ],
            style_header={
                'backgroundColor': '#F8F7F4'
            },
            filtering=True,

        ),
        className="row",
        style={
            'width': '50%',
        },
    ),
]

# hide/show modal
@app.callback(Output("trans_modal", "style"), [Input("add-new-btn", "n_clicks")])
def display_trans_modal_callback(n):
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}

# reset to 0 add button n_clicks property 
@app.callback(
    Output("add-new-btn", "n_clicks"),
    [Input("modal_close", "n_clicks"), Input("submit-btn", "n_clicks")],
)
def close_modal_callback(n, n2):
    return 0

# add new transaction
@app.callback(
    Output('trans-df', 'data'),
    [Input('add-new-btn', 'n_clicks')],
    [
        State('category', 'value'),
        State('place', 'value'),
        State('purchase-date', 'date'),
        State('amount', 'value'),
        State('city', 'value')
    ]
)
def update_df(n_clicks, category, place, date, amount, city):
    if n_clicks == 0: 
        df = pd.read_csv('transactions.csv')
        return df.to_dict('records')
    else:
        if amount == "":
            df = pd.read_csv('transactions.csv')
            return df.to_dict('records')
        else:
            tmp = pd.DataFrame({'amount': [amount], 'Date': [date], 'Place': [place], 'City': [city], 'Category': [category]})
            with open('transactions.csv', 'a') as f:
                            tmp.to_csv(f, header=False)
            df = pd.read_csv('transactions.csv')
            return df.to_dict('records')

