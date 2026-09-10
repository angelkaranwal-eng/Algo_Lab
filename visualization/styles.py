"""
Consistent color palette, theme constants, and visual state styling.
"""

PALETTE = {
    'bg_primary': '#0D1117',
    'bg_card': '#161B22',
    'bg_card_secondary': '#21262D',
    'border': '#30363D',
    'text_primary': '#F0F6FC',
    'text_secondary': '#8B949E',
    'accent_blue': '#58A6FF',
    'accent_green': '#3FB950',
    'accent_orange': '#D29922',
    'accent_red': '#F85149',
    'accent_purple': '#BC8CFF',
    'neutral_bar': '#388BFD',
    'highlight': '#F1E05A',
    'sorted': '#2EA043',
    'active': '#FF7B72',
}

APP_STYLESHEET = f"""
QMainWindow {{
    background-color: {PALETTE['bg_primary']};
}}
QWidget {{
    background-color: {PALETTE['bg_primary']};
    color: {PALETTE['text_primary']};
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
}}
QFrame#card {{
    background-color: {PALETTE['bg_card']};
    border: 1px solid {PALETTE['border']};
    border-radius: 8px;
    padding: 12px;
}}
QPushButton {{
    background-color: {PALETTE['bg_card_secondary']};
    color: {PALETTE['text_primary']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {PALETTE['border']};
    border-color: {PALETTE['accent_blue']};
}}
QPushButton:pressed {{
    background-color: {PALETTE['accent_blue']};
    color: #FFFFFF;
}}
QPushButton:disabled {{
    color: {PALETTE['text_secondary']};
    background-color: {PALETTE['bg_card']};
    border-color: {PALETTE['border']};
}}
QPushButton#action_btn {{
    background-color: {PALETTE['neutral_bar']};
    color: #FFFFFF;
    border: none;
}}
QPushButton#action_btn:hover {{
    background-color: {PALETTE['accent_blue']};
}}
QComboBox, QSpinBox, QLineEdit {{
    background-color: {PALETTE['bg_card_secondary']};
    color: {PALETTE['text_primary']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    padding: 5px 10px;
}}
QComboBox::drop-down {{
    border: none;
}}
QSlider::groove:horizontal {{
    height: 6px;
    background: {PALETTE['bg_card_secondary']};
    border-radius: 3px;
}}
QSlider::sub-page:horizontal {{
    background: {PALETTE['accent_blue']};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {PALETTE['text_primary']};
    width: 14px;
    margin-top: -4px;
    margin-bottom: -4px;
    border-radius: 7px;
}}
QTableWidget {{
    background-color: {PALETTE['bg_card']};
    gridline-color: {PALETTE['border']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
}}
QHeaderView::section {{
    background-color: {PALETTE['bg_card_secondary']};
    color: {PALETTE['text_primary']};
    padding: 6px;
    border: 1px solid {PALETTE['border']};
    font-weight: bold;
}}
QScrollBar:vertical {{
    background: {PALETTE['bg_primary']};
    width: 8px;
}}
QScrollBar::handle:vertical {{
    background: {PALETTE['border']};
    border-radius: 4px;
}}
"""