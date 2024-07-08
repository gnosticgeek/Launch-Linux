import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QProgressBar, QInputDialog,
                             QLineEdit, QMessageBox, QHBoxLayout, QSpacerItem,
                             QSizePolicy)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon

# Catppuccin Latte color palette
COLORS = {
    'rosewater': '#dc8a78',
    'flamingo': '#dd7878',
    'pink': '#ea76cb',
    'mauve': '#8839ef',
    'red': '#d20f39',
    'maroon': '#e64553',
    'peach': '#fe640b',
    'yellow': '#df8e1d',
    'green': '#40a02b',
    'teal': '#179299',
    'sky': '#04a5e5',
    'sapphire': '#209fb5',
    'blue': '#1e66f5',
    'lavender': '#7287fd',
    'text': '#4c4f69',
    'subtext1': '#5c5f77',
    'subtext0': '#6c6f85',
    'overlay2': '#7c7f93',
    'overlay1': '#8c8fa1',
    'overlay0': '#9ca0b0',
    'surface2': '#acb0be',
    'surface1': '#bcc0cc',
    'surface0': '#ccd0da',
    'base': '#eff1f5',
    'mantle': '#e6e9ef',
    'crust': '#dce0e8',
}

class DependencyInstaller(QThread):
    update_progress = pyqtSignal(int)
    update_status = pyqtSignal(str)
    update_detail = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    installation_complete = pyqtSignal()

    def __init__(self, sudo_password):
        super().__init__()
        self.sudo_password = sudo_password
        self.dependencies = ['git', 'curl', 'ansible']

    def run_sudo_command(self, command):
        full_command = f"echo {self.sudo_password} | sudo -S {command}"
        try:
            process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.update_detail.emit(output.strip())
            if process.returncode != 0:
                raise Exception(f"Command failed with return code {process.returncode}")
        except Exception as e:
            raise Exception(f"Command failed: {str(e)}")

    def run(self):
        try:
            self.update_status.emit("Updating package lists...")
            self.run_sudo_command("apt-get update")
            self.update_progress.emit(20)

            for i, dep in enumerate(self.dependencies):
                self.update_status.emit(f"Installing {dep}...")
                self.run_sudo_command(f"apt-get install -y {dep}")
                progress = 20 + int((i + 1) / len(self.dependencies) * 80)
                self.update_progress.emit(progress)

            self.update_status.emit("All dependencies installed successfully!")
            self.installation_complete.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

class LaunchGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Launch - Linux Setup Assistant")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['base']};
            }}
            QLabel {{
                color: {COLORS['text']};
            }}
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
            QPushButton:hover {{
                background-color: {COLORS['sapphire']};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['surface1']};
                color: {COLORS['overlay1']};
            }}
            QProgressBar {{
                border: 2px solid {COLORS['blue']};
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['blue']};
            }}
        """)

        main_layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("Welcome to Launch!")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; margin: 20px 0; color: {COLORS['mauve']};")
        main_layout.addWidget(self.title_label)

        # Description
        self.description_label = QLabel(
            "Launch is your friendly Linux setup assistant. We'll guide you through "
            "the process of setting up your system with essential tools and "
            "optimized configurations, making your Linux experience smooth and enjoyable."
        )
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(f"font-size: 14px; margin: 10px 20px; color: {COLORS['subtext0']};")
        main_layout.addWidget(self.description_label)

        # Status
        self.status_label = QLabel("Ready to install dependencies.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"font-size: 18px; margin-bottom: 10px; color: {COLORS['text']};")
        main_layout.addWidget(self.status_label)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Detailed Status
        self.detail_label = QLabel("")
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail_label.setStyleSheet(f"font-size: 14px; color: {COLORS['subtext1']}; margin-top: 10px;")
        self.detail_label.setWordWrap(True)
        main_layout.addWidget(self.detail_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.start_button = QPushButton("Start Installation")
        self.start_button.clicked.connect(self.start_installation)
        self.start_button.setIcon(QIcon('path/to/start_icon.png'))  # Add an icon
        button_layout.addWidget(self.start_button)

        self.next_button = QPushButton("Next Step")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setEnabled(False)
        self.next_button.setIcon(QIcon('path/to/next_icon.png'))  # Add an icon
        button_layout.addWidget(self.next_button)

        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def start_installation(self):
        password, ok = QInputDialog.getText(self, 'Sudo Password',
                                            'Enter your sudo password:',
                                            QLineEdit.EchoMode.Password)
        if ok:
            self.start_button.setEnabled(False)
            self.installer = DependencyInstaller(password)
            self.installer.update_progress.connect(self.update_progress)
            self.installer.update_status.connect(self.update_status)
            self.installer.update_detail.connect(self.update_detail)
            self.installer.error_occurred.connect(self.show_error)
            self.installer.installation_complete.connect(self.installation_complete)
            self.installer.start()
        else:
            self.status_label.setText("Installation cancelled.")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, status):
        self.status_label.setText(status)

    def update_detail(self, detail):
        self.detail_label.setText(detail)

    def show_error(self, error_message):
        QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")
        self.start_button.setEnabled(True)

    def installation_complete(self):
        self.next_button.setEnabled(True)
        self.status_label.setText("Dependencies installed successfully!")
        self.detail_label.setText("You're ready for the next step!")
        QMessageBox.information(self, "Success", "Dependencies installed successfully!")

    def next_step(self):
        QMessageBox.information(self, "Next Step", "Ready for the next step of the setup process!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LaunchGUI()
    window.show()
    sys.exit(app.exec())
