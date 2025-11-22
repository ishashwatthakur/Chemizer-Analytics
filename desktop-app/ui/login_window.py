import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox,
    QGraphicsBlurEffect, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

from api.django_client import api_client
from ui.signup_window import SignupWindow
from ui.main_window import MainWindow
from ui.otp_dialog import OTPDialog
from ui.error_dialog import ErrorDialog


class LoginWindow(QMainWindow):
    BASE_WIDTH = 1200
    BASE_HEIGHT = 800

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Chemizer Analytics")
        self.setGeometry(100, 100, self.BASE_WIDTH, self.BASE_HEIGHT) 
        
        self.showMaximized()
        
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(self.central_widget)
        
        self.diagram_data = [
            {"text": "H₂O", "font_size": 48, "pos": (50, 150)},
            {"text": "⚙️", "font_size": 54, "pos": (150, 300)},
            {"text": "📊", "font_size": 51, "pos": (250, 100)},
            {"text": "🔬", "font_size": 48, "pos": (100, 500)},
            {"text": "🧪", "font_size": 54, "pos": (300, 600)},
            {"text": "📈", "font_size": 51, "pos": (50, 650)},    
            {"text": "⚗️", "font_size": 48, "pos": (800, 120)},
            {"text": "🌡️", "font_size": 54, "pos": (900, 250)},
            {"text": "💧", "font_size": 51, "pos": (1000, 80)},
            {"text": "🔍", "font_size": 48, "pos": (1100, 400)},
            {"text": "📋", "font_size": 54, "pos": (950, 620)},   
            {"text": "⚡", "font_size": 51, "pos": (850, 500)},
            {"text": "🌀", "font_size": 48, "pos": (1050, 700)},  
        ]
        
        self.diagram_labels = []
        for data in self.diagram_data:
            label = self.create_blurred_label(data["text"], data["font_size"])
            label.setParent(self.central_widget)
            self.diagram_labels.append(label)

        self.top_bar_widget = QWidget(self.central_widget)
        self.top_bar_widget.setStyleSheet("background: transparent;")
        top_bar_layout = QHBoxLayout(self.top_bar_widget)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        site_name = QLabel("Chemizer Analytics")
        site_name.setFont(QFont("Comic Sans MS", 36, QFont.Bold)) 
        site_name.setStyleSheet("color: black;")
        
        top_bar_layout.addWidget(site_name)
        top_bar_layout.addStretch(1)

        self.login_form_widget = QWidget(self.central_widget)
        self.login_form_widget.setMaximumWidth(500)
        self.login_form_widget.setMinimumWidth(450)
        self.login_form_widget.setStyleSheet("background: transparent;")
        
        login_layout = QVBoxLayout(self.login_form_widget)
        login_layout.setContentsMargins(10, 10, 10, 10)
        login_layout.setSpacing(15)

        login_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        title = QLabel("Sign In")
        title.setFont(QFont("Comic Sans MS", 32, QFont.Bold)) 
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #000000;")
        login_layout.addWidget(title)
        
        subtitle = QLabel("Enter your credentials to access your account")
        subtitle.setFont(QFont("Comic Sans MS", 13))
        subtitle.setStyleSheet("color: #666666;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        login_layout.addWidget(subtitle)
        
        login_layout.addSpacing(30)
        
        username_label = QLabel("Username")
        username_label.setFont(QFont("Inter", 11))
        username_label.setStyleSheet("color: #000000;")
        login_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont("Inter", 11))
        self.username_input.setFixedHeight(50)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #00BFFF;
            }
        """)
        login_layout.addWidget(self.username_input)
        
        password_label = QLabel("Password")
        password_label.setFont(QFont("Inter", 11))
        password_label.setStyleSheet("color: #000000;")
        login_layout.addWidget(password_label)

        self.password_container = QWidget()
        self.password_container.setFixedHeight(50)
        self.password_container.setStyleSheet("""
            QWidget {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
            }
        """)
        
        password_field_layout = QHBoxLayout(self.password_container)
        password_field_layout.setContentsMargins(12, 0, 5, 0)
        password_field_layout.setSpacing(5)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Inter", 11))
        self.password_input.setStyleSheet("border: none; background: transparent;")

        self.show_password_button = QPushButton("Show")
        self.show_password_button.setFont(QFont("Inter", 10))
        self.show_password_button.setCheckable(True)
        self.show_password_button.setStyleSheet("""
            QPushButton {
                color: #00BFFF; 
                border: none; 
                background: transparent;
                padding-right: 5px;
            }
        """)
        self.show_password_button.toggled.connect(self.toggle_password_visibility)
        
        password_field_layout.addWidget(self.password_input, 1) 
        password_field_layout.addWidget(self.show_password_button)
        
        self.password_input.focusInEvent = lambda e, pc=self.password_container: self.set_focus_style(pc, True)
        self.password_input.focusOutEvent = lambda e, pc=self.password_container: self.set_focus_style(pc, False)

        login_layout.addWidget(self.password_container) 
        
        login_layout.addSpacing(10)

        self.signin_btn = QPushButton("Sign In")
        self.signin_btn.setFont(QFont("Inter", 12, QFont.Bold))
        self.signin_btn.setCursor(Qt.PointingHandCursor)
        self.signin_btn.setStyleSheet("""
            QPushButton {
                padding: 14px;
                background-color: #111111;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        self.signin_btn.clicked.connect(self.handle_signin)
        login_layout.addWidget(self.signin_btn)
        
        login_layout.addSpacing(10)

        signup_layout = QVBoxLayout()
        signup_layout.setSpacing(5)
        
        signup_label = QLabel("Don't have an account?")
        signup_label.setFont(QFont("Inter", 10))
        signup_label.setStyleSheet("color: #333333;")
        signup_label.setAlignment(Qt.AlignCenter)
        signup_layout.addWidget(signup_label)
        
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setFont(QFont("Inter", 10, QFont.Bold))
        self.signup_btn.setCursor(Qt.PointingHandCursor)
        self.signup_btn.setStyleSheet("""
            QPushButton {
                color: #00BFFF;
                border: none;
                background: transparent;
                max-width: 100px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.signup_btn.clicked.connect(self.show_signup)
        signup_layout.addWidget(self.signup_btn, 0, Qt.AlignCenter)
        
        login_layout.addLayout(signup_layout)

        login_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.resizeEvent(None)
    
    def resizeEvent(self, event):
        if not hasattr(self, 'top_bar_widget'):
            if event:
                super().resizeEvent(event)
            return

        w = self.width()
        h = self.height()
        
        self.top_bar_widget.setGeometry(30, 5, w - 60, 110)

        form_w = self.login_form_widget.maximumWidth()
        form_h = self.login_form_widget.sizeHint().height()
        if form_h < 600: 
            form_h = 600
        
        form_x = (w - form_w) // 2
        form_y = (h - form_h) // 2
        if form_y < 60: 
            form_y = 60
        
        self.login_form_widget.setGeometry(form_x, form_y, form_w, form_h)

        scale_x = w / self.BASE_WIDTH
        scale_y = h / self.BASE_HEIGHT
        
        for i, label in enumerate(self.diagram_labels):
            data = self.diagram_data[i]
            orig_pos = data["pos"]
            
            new_x = int(orig_pos[0] * scale_x)
            new_y = int(orig_pos[1] * scale_y)
            
            label.move(new_x, new_y)
        
        self.login_form_widget.raise_()
        self.top_bar_widget.raise_()
        
        if event:
            super().resizeEvent(event)

    def create_blurred_label(self, text, font_size):
        label = QLabel(text)
        label.setFont(QFont("Inter", font_size))
        label.setStyleSheet("color: rgba(0, 191, 255, 0.5); background: transparent;") 
        
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(1) 
        label.setGraphicsEffect(blur_effect)
        
        return label

    def set_focus_style(self, widget, has_focus):
        if has_focus:
            widget.setStyleSheet("""
                QWidget {
                    border: 2px solid #00BFFF;
                    border-radius: 8px;
                    background-color: white;
                }
            """)
        else:
            widget.setStyleSheet("""
                QWidget {
                    border: 2px solid #e5e7eb;
                    border-radius: 8px;
                    background-color: white;
                }
            """)

    def toggle_password_visibility(self, toggled): 
        if toggled:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")

    def handle_signin(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            error_dialog = ErrorDialog("Login Error", "Please fill in all fields.", self)
            error_dialog.exec_()
            return
        
        print(f"UI: Calling API to login with {username}")
        response = api_client.login(username, password)
        
        if "error" in response:
            friendly_message = "Invalid Credentials.\n\nPlease check your username and password and try again."
            
            error_dialog = ErrorDialog("Login Failed", friendly_message, self)
            error_dialog.exec_()
        elif "requires_otp" in response and response["requires_otp"]:
            print(f"UI: OTP required for {response['email']}")
            otp_dialog = OTPDialog(response["email"], api_client, self)
            if otp_dialog.exec_():
                print("UI: OTP dialog accepted, opening main window.")
                self.open_main_window()
            else:
                print("UI: OTP dialog was cancelled or failed.")
                error_dialog = ErrorDialog("OTP Failed", "OTP verification was not successful. Please try logging in again.", self)
                error_dialog.exec_()
        else:
            error_dialog = ErrorDialog("Server Error", "An invalid response was received from the server. Please try again later.", self)
            error_dialog.exec_()

    def show_signup(self):
        print("UI: Opening signup window.")
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()

    def open_main_window(self):
        print("UI: Opening main window.")
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()