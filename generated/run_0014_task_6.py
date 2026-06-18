from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, server=Flask(__name__))

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Hello, Dash!"),
    dcc.Input(id='input-box', type='text', value='Enter something'),
    html.Div(id='output-container')
])

# Define a callback to update the output based on input
@app.callback(
    Output('output-container', 'children'),
    [Input('input-box', 'value')]
)
def update_output(value):
    return f'You entered: {value}'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
