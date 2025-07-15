from dash import Input, Output, html
from app import app

from pages.coal import layout_coal
from pages.gas import layout_gas
from pages.oil import layout_oil

@app.callback(
    Output('main-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    pages = {
        "/coal": layout_coal,
        "/gas": layout_gas,
        "/oil": layout_oil
    }
    layout_func = pages.get(pathname)
    if layout_func:
        return layout_func()
    return html.Div([
        html.H3("404 – Seite nicht gefunden"),
        html.P(f"Die Seite „{pathname}“ existiert nicht.")
    ])