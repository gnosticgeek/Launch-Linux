import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QProgressBar, QInputDialog,
                             QLineEdit, QMessageBox, QHBoxLayout, QSpacerItem,
                             QSizePolicy, QComboBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QIcon

from lib import catppuccin_latte, tokyo_night_moon

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
            for output in process.stdout:
                self.update_detail.emit(output.strip())
            if process.wait() != 0:
                raise subprocess.CalledProcessError(process.returncode, command)
        except Exception as e:
            raise Exception(f"Command failed: {str(e)}")

    def run(self):
        try:
            self.update_status.emit("Updating package lists...")
            self.run_sudo_command("apt-get update")
            self.update_progress.emit(20)

            for i, dep in enumerate(self.dependencies, 1):
                self.update_status.emit(f"Installing {dep}...")
                self.run_sudo_command(f"apt-get install -y {dep}")
                self.update_progress.emit(20 + int(i / len(self.dependencies) * 80))

            self.update_status.emit("All dependencies installed successfully!")
            self.installation_complete.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

class LaunchGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.themes = {
            "Catppuccin Latte": catppuccin_latte,
            "Tokyo Night Moon": tokyo_night_moon
        }
        self.current_theme = "Catppuccin Latte"
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Launch - Linux Setup Assistant")
        self.setGeometry(100, 100, 600, 500)
        self.update_theme()

        main_layout = QVBoxLayout()

        # Theme switcher
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.themes.keys())
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        main_layout.addWidget(self.create_label("Welcome to Launch!", 24, 'mauve', bold=True, margin="20px 0"))
        main_layout.addWidget(self.create_label(
            "Launch is your friendly Linux setup assistant. We'll guide you through "
            "the process of setting up your system with essential tools and "
            "optimized configurations, making your Linux experience smooth and enjoyable.",
            14, 'subtext0', align=Qt.AlignmentFlag.AlignCenter, margin="10px 20px", wrap=True
        ))

        self.status_label = self.create_label("Ready to install dependencies.", 18, 'text', margin="0 0 10px 0")
        main_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.detail_label = self.create_label("", 14, 'subtext1', margin="10px 0 0 0", wrap=True)
        main_layout.addWidget(self.detail_label)

        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.start_button = self.create_button("Start Installation", self.start_installation, 'path/to/start_icon.png')
        button_layout.addWidget(self.start_button)

        self.next_button = self.create_button("Next Step", self.next_step, 'path/to/next_icon.png')
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.next_button)

        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_label(self, text, size, color, bold=False, align=Qt.AlignmentFlag.AlignCenter, margin="0", wrap=False):
        label = QLabel(text)
        label.setAlignment(align)
        label.setStyleSheet(f"font-size: {size}px; color: {self.themes[self.current_theme].COLORS[color]}; margin: {margin}; "
                            f"font-weight: {'bold' if bold else 'normal'};")
        if wrap:
            label.setWordWrap(True)
        return label

    def create_button(self, text, callback, icon_path):
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setIcon(QIcon(icon_path))
        return button

    def update_theme(self):
        self.setStyleSheet(self.themes[self.current_theme].get_stylesheet())

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.update_theme()
        # Update existing widgets' colors
        self.status_label.setStyleSheet(f"font-size: 18px; color: {self.themes[self.current_theme].COLORS['text']}; margin: 0 0 10px 0;")
        self.detail_label.setStyleSheet(f"font-size: 14px; color: {self.themes[self.current_theme].COLORS['subtext1']}; margin: 10px 0 0 0;")

    def start_installation(self):
        password, ok = QInputDialog.getText(self, 'Sudo Password',
                                            'Enter your sudo password:',
                                            QLineEdit.EchoMode.Password)
        if ok:
            self.start_button.setEnabled(False)
            self.installer = DependencyInstaller(password)
            self.installer.update_progress.connect(self.progress_bar.setValue)
            self.installer.update_status.connect(self.status_label.setText)
            self.installer.update_detail.connect(self.detail_label.setText)
            self.installer.error_occurred.connect(self.show_error)
            self.installer.installation_complete.connect(self.installation_complete)
            self.installer.start()
        else:
            self.status_label.setText("Installation cancelled.")

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