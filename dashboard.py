import dash
from dash import html 

app = dash.Dash(name)

app.layout = html.Div([
    html.H1(children='PROJECT ZAGADKA')
])

if name == 'main':
    app.run_server(debug=True)