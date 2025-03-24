

node_widget_style = """
   #NodeWidget {
        background-color: black;
   }

   #NodeLabelArea {
        background-color: grey;
   }

   #NodeLabelText {
        font-weight: bold;
        font-size: 14px;
   }

   #NodeNameText {
        font-weight: normal;
        font-size: 10px;
   }

   #NodeArea {
        background-color: #303030;
   }
"""

node_selected_widget_style = """
   #NodeWidget {
        background-color: orange;
   }

   #NodeLabelArea {
        background-color: grey;
   }

   #NodeLabelText {
        font-weight: bold;
        font-size: 14px;
   }

   #NodeNameText {
        font-weight: normal;
        font-size: 10px;
   }

   #NodeArea {
        background-color: #303030;
   }
"""

app_style = """
    QMainWindow {
        background-color: rgb(25, 5, 25);
    }

    QGraphicsView {
        background-color: rgb(40, 10, 30);
    }

    QListWidget {
        background-color: rgb(40, 10, 30)
    }

    QListItemWidget {
        background-color: white;
    }

    #LogView {
        background-color: rgb(40, 10, 30);
        color: rgb(160, 160, 160);
        font-family: "Fira Code";
        font-size: 12px;
        font-weight: bold;
        line-height: 1.0;
    }

    #PropertyPanelWidget QGroupBox QLabel {
        color: rgb(180, 180, 180);
    }
"""


THEME_APP_PRIMARY_COLOR: str = "rgb(24, 24, 24)"
THEME_APP_SECONDARY_COLOR: str = "rgb(28, 28, 28)"
THEME_TEXT_PRMIARY_COLOR: str = "rgb(220, 220, 220)"
THEME_TEXT_SECONDARY_COLOR: str = "rgb(180, 180, 180)"
THEME_TEXT_SECONDARY_COLOR: str = "rgb(180, 180, 180)"
THEME_PRMIARY_DARK_COLOR: str = "rgb(36, 36, 36)"
THEME_SECONDARY_DARK_COLOR: str = "rgb(42, 42, 42)"
THEME_PRMIARY_LIGHT_COLOR: str = "rgb(180, 180, 180)"
THEME_SECONDARY_LIGHT_COLOR: str = "rgb(180, 180, 180)"
THEME_PRMIARY_ACCENT_COLOR: str = "rgb(200, 100, 20)"
THEME_SECONDARY_ACCENT_COLOR: str = "rgb(200, 144, 90)"

theme_style = f"""

    QMainWindow {{
        background-color: {THEME_APP_PRIMARY_COLOR};
    }}

    QFrame {{
        border              : 2px solid {THEME_PRMIARY_DARK_COLOR};
        border-radius       : 2px;
        padding             : 0px;
    }}

    #PropertyPanelWidget QGroupBox {{
        background-color    : {THEME_SECONDARY_DARK_COLOR};
        padding             : 0px;
    }}

    #PropertyPanelWidget QGroupBox {{
        color               : {THEME_SECONDARY_ACCENT_COLOR};
        padding             : 0px;
        font-size           : 16px;
        font-weight         : bold;
    }}

    CommonWidget {{

    }}

    CommonWidget QLabel {{
        color               : {THEME_TEXT_PRMIARY_COLOR};
        font-size           : 16px;
        font-weight         : bold;
    }}

    CommonWidget QFrame {{
        border              : 0px;
        padding             : 0px;
    }}

    CommonWidget QLineEdit, QDoubleSpinBox {{
        background-color    : {THEME_PRMIARY_DARK_COLOR};
        color               : {THEME_TEXT_SECONDARY_COLOR};
    }}

    QGraphicsView {{
        background-color    : {THEME_APP_SECONDARY_COLOR};
    }}

    #LogView {{
        background-color    : {THEME_PRMIARY_DARK_COLOR};
        color               : {THEME_TEXT_SECONDARY_COLOR};
        font-family         : "Fira Code";
        font-size           : 12px;
        font-weight         : bold;
        line-height         : 1.0;
    }}

    NodePaletteWidget {{
        background-color    : {THEME_PRMIARY_DARK_COLOR};
    }}

    NodePaletteWidget QListWidget {{
        background-color    : {THEME_PRMIARY_DARK_COLOR};
        font-family         : "Fira Code";
        font-size           : 12px;
        color               : {THEME_TEXT_PRMIARY_COLOR};
    }}
"""
