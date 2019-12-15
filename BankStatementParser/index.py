# the index file of the application where the app navigates from

# necessary imports
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output

# import the pages (apps) & import app
from apps import budget_manager, hist_trans_tab
from app import app

app.layout = html.Div([
    dcc.Tabs(
        id='tabs',
        value = 'hist_trans_tab',
        children=[
            dcc.Tab(
                label = 'Historical Transactions',
                value = 'hist_trans_tab'
            ),
            dcc.Tab(
                label = 'Budget Manager',
                value = 'budget_manager'
            )
        ]
    ),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('tabs', 'value')]
)
def display_page(tab_value):
    if tab_value == 'budget_manager':
        return budget_manager.layout
    elif tab_value == 'hist_trans_tab':
        return hist_trans_tab.layout
    else: 
        return budget_manager.layout

if __name__ == '__main__':
    app.run_server(debug=True)