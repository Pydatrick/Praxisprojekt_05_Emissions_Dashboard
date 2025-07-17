from dash import Input, Output, html
from app import app

from pages.home import layout_home
from pages.coal import layout_coal
from pages.gas import layout_gas
from pages.oil import layout_oil
from pages.landuse import layout_landuse
from pages.total import layout_total
from pages.per_capita import layout_per_capita

@app.callback(
    Output('main-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    pages = {
        "/" : layout_home,
        "/total" : layout_total,
        "/coal": layout_coal,
        "/gas": layout_gas,
        "/oil": layout_oil,
        "/landuse": layout_landuse,
        "/per_capita" : layout_per_capita
    }
    layout_func = pages.get(pathname)
    if layout_func:
        return layout_func()
    return html.Div([
        html.H3("404 – Seite nicht gefunden"),
        html.P(f"Die Seite „{pathname}“ existiert nicht.")
    ])