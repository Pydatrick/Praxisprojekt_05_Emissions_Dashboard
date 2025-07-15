from app import app
from layout.main_layout import create_layout

# WICHTIG, damit dash die callbacks kennt
import callbacks.router 
import callbacks.sidebar_toggle

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)