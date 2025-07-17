from app import app
from layout.main_layout import create_layout

# WICHTIG, damit dash die callbacks kennt
import callbacks.router 
import callbacks.sidebar_toggle
import callbacks.coal_plot
import callbacks.gas_plot
import callbacks.landuse_plot
import callbacks.oil_plot
import callbacks.total_plot

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)