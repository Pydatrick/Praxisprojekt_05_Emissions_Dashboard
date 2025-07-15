from app import app
from layout.main_layout2 import create_layout
import callbacks.callback_test  # nur um Callback-Registrierung zu triggern

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)


