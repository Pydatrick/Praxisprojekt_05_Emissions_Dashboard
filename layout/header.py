from dash import html

def create_header():
    return html.Div([ 
           html.H1(["CO", html.Sub("2"), " Emissionen Dashboard"
                    ], className="header-title",)
    ], className="header",)