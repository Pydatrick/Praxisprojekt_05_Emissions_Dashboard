# Projekt-Emission-Dashboard
dashboards und co

projekt/
│
├── assets/
│   └── styles.css                   # Wird automatisch von Dash geladen
│
├── callbacks/
│   └── callback_test.py            # Callbacks separat, gute Praxis
│
├── data/
│   └── raw/                        # CSV-Daten hier lagern
│
├── layout/
│   ├── header.py                   # z.B. Navbar, Titel etc.
│   ├── sidebar.py                  # z.B. Länderauswahl etc.
│   └── main_layout.py              # verbindet Header, Sidebar und Main Content
│
├── app.py                          # Initialisiert die Dash-Instanz
├── main.py                         # Einstiegspunkt (setzt Layout & startet App)