COLORS = {
    'rosewater': '#dc8a78', 'flamingo': '#dd7878', 'pink': '#ea76cb',
    'mauve': '#8839ef', 'red': '#d20f39', 'maroon': '#e64553',
    'peach': '#fe640b', 'yellow': '#df8e1d', 'green': '#40a02b',
    'teal': '#179299', 'sky': '#04a5e5', 'sapphire': '#209fb5',
    'blue': '#1e66f5', 'lavender': '#7287fd', 'text': '#4c4f69',
    'subtext1': '#5c5f77', 'subtext0': '#6c6f85', 'overlay2': '#7c7f93',
    'overlay1': '#8c8fa1', 'overlay0': '#9ca0b0', 'surface2': '#acb0be',
    'surface1': '#bcc0cc', 'surface0': '#ccd0da', 'base': '#eff1f5',
    'mantle': '#e6e9ef', 'crust': '#dce0e8',
}

def get_stylesheet():
    return f"""
        QMainWindow {{ background-color: {COLORS['base']}; }}
        QLabel {{ color: {COLORS['text']}; }}
        QPushButton {{
            background-color: {COLORS['blue']};
            color: {COLORS['base']};
            border: none;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 5px;
        }}
        QPushButton:hover {{ background-color: {COLORS['sapphire']}; }}
        QPushButton:disabled {{
            background-color: {COLORS['surface1']};
            color: {COLORS['overlay1']};
        }}
        QProgressBar {{
            border: 2px solid {COLORS['blue']};
            border-radius: 5px;
            text-align: center;
        }}
        QProgressBar::chunk {{ background-color: {COLORS['blue']}; }}
        QComboBox {{
            background-color: {COLORS['surface0']};
            color: {COLORS['text']};
            border: 1px solid {COLORS['overlay0']};
            padding: 5px;
            border-radius: 3px;
        }}
        QComboBox:hover {{ border-color: {COLORS['blue']}; }}
        QComboBox::drop-down {{ width: 20px; }}
        QComboBox::down-arrow {{ image: url(path/to/down_arrow.png); }}
    """