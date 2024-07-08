COLORS = {
    'bg': '#222436', 'fg': '#c8d3f5', 'red': '#ff757f',
    'orange': '#ff966c', 'yellow': '#ffc777', 'green': '#c3e88d',
    'cyan': '#86e1fc', 'blue': '#82aaff', 'purple': '#c099ff',
    'bg_dark': '#1e2030', 'bg_highlight': '#2f334d', 'comment': '#7a88cf',
    'terminal_black': '#444a73', 'line': '#3b4261'
}

def get_stylesheet():
    return f"""
        QMainWindow {{ background-color: {COLORS['bg']}; }}
        QLabel {{ color: {COLORS['fg']}; }}
        QPushButton {{
            background-color: {COLORS['blue']};
            color: {COLORS['bg']};
            border: none;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 5px;
        }}
        QPushButton:hover {{ background-color: {COLORS['purple']}; }}
        QPushButton:disabled {{
            background-color: {COLORS['terminal_black']};
            color: {COLORS['comment']};
        }}
        QProgressBar {{
            border: 2px solid {COLORS['blue']};
            border-radius: 5px;
            text-align: center;
        }}
        QProgressBar::chunk {{ background-color: {COLORS['blue']}; }}
        QComboBox {{
            background-color: {COLORS['bg_highlight']};
            color: {COLORS['fg']};
            border: 1px solid {COLORS['line']};
            padding: 5px;
            border-radius: 3px;
        }}
        QComboBox:hover {{ border-color: {COLORS['blue']}; }}
        QComboBox::drop-down {{ width: 20px; }}
        QComboBox::down-arrow {{ image: url(path/to/down_arrow.png); }}
    """