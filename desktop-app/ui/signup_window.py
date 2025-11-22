import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QDateEdit, QMessageBox, QScrollArea, QGraphicsBlurEffect,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QFont

from api.django_client import api_client
from ui.otp_dialog import OTPDialog


class SignupWindow(QMainWindow):
    BASE_WIDTH = 1200
    BASE_HEIGHT = 800

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up - Chemizer Analytics")
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

        self.signup_form_widget = QWidget(self.central_widget)
        self.signup_form_widget.setMaximumWidth(550)
        self.signup_form_widget.setMinimumWidth(500)
        self.signup_form_widget.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(self.signup_form_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        title = QLabel("Create Account")
        title.setFont(QFont("Comic Sans MS", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #000000;")
        layout.addWidget(title)
        
        subtitle = QLabel("Fill in the details to create your account")
        subtitle.setFont(QFont("Comic Sans MS", 13))
        subtitle.setStyleSheet("color: #666666;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background: transparent; 
            } 
            QScrollBar:vertical { 
                border: none; 
                background: #e0e0e0; 
                width: 8px; 
                margin: 0px 0px 0px 0px; 
            } 
            QScrollBar::handle:vertical { 
                background: #00BFFF; 
                min-height: 20px; 
                border-radius: 4px; 
            } 
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { 
                border: none; 
                background: none; 
                height: 0px; 
            }
        """)
        layout.addWidget(self.scroll_area)

        self.scroll_content_widget = QWidget()
        self.scroll_content_widget.setStyleSheet("background: transparent;")
        self.scroll_area.setWidget(self.scroll_content_widget)

        scroll_layout = QVBoxLayout(self.scroll_content_widget)
        scroll_layout.setContentsMargins(0, 0, 5, 0)
        scroll_layout.setSpacing(15)

        scroll_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        fullname_label = QLabel("Full Name")
        fullname_label.setFont(QFont("Inter", 11))
        scroll_layout.addWidget(fullname_label)
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter your full name")
        self.fullname_input.setFont(QFont("Inter", 11))
        self.fullname_input.setFixedHeight(50)
        self.fullname_input.setStyleSheet(self.input_style())
        scroll_layout.addWidget(self.fullname_input)
        
        username_label = QLabel("Username")
        username_label.setFont(QFont("Inter", 11))
        scroll_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setFont(QFont("Inter", 11))
        self.username_input.setFixedHeight(50)
        self.username_input.setStyleSheet(self.input_style())
        scroll_layout.addWidget(self.username_input)
        
        email_label = QLabel("Email")
        email_label.setFont(QFont("Inter", 11))
        scroll_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setFont(QFont("Inter", 11))
        self.email_input.setFixedHeight(50)
        self.email_input.setStyleSheet(self.input_style())
        scroll_layout.addWidget(self.email_input)
        
        dob_label = QLabel("Date of Birth")
        dob_label.setFont(QFont("Inter", 11))
        scroll_layout.addWidget(dob_label)
        self.dob_input = QDateEdit()
        self.dob_input.setDate(QDate(2000, 1, 1))
        self.dob_input.setCalendarPopup(True)
        
        self.dob_input.setFocusPolicy(Qt.StrongFocus)
        self.dob_input.wheelEvent = lambda event: None
        
        self.dob_input.setFont(QFont("Inter", 11))
        self.dob_input.setFixedHeight(50)
        self.dob_input.setStyleSheet(self.input_style())
        scroll_layout.addWidget(self.dob_input)
        
        gender_label = QLabel("Gender")
        gender_label.setFont(QFont("Inter", 11))
        scroll_layout.addWidget(gender_label)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Select gender", "Male", "Female", "Other", "Prefer not to say"])
        
        self.gender_combo.setFocusPolicy(Qt.StrongFocus)
        self.gender_combo.wheelEvent = lambda event: None
        
        self.gender_combo.setFont(QFont("Inter", 11))
        self.gender_combo.setFixedHeight(50)
        self.gender_combo.setStyleSheet(self.input_style())
        scroll_layout.addWidget(self.gender_combo)
        
        password_label = QLabel("Password")
        password_label.setFont(QFont("Inter", 11))
        password_label.setStyleSheet("color: #000000;")
        scroll_layout.addWidget(password_label)

        self.password_container = QWidget()
        self.password_container.setFixedHeight(50)
        self.password_container.setStyleSheet(self.password_container_style(focused=False))
        password_field_layout = QHBoxLayout(self.password_container)
        password_field_layout.setContentsMargins(12, 0, 5, 0)
        password_field_layout.setSpacing(5)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Inter", 11))
        self.password_input.setStyleSheet("border: none; background: transparent;")

        self.show_password_button = QPushButton("Show")
        self.show_password_button.setFont(QFont("Inter", 10))
        self.show_password_button.setCheckable(True)
        self.show_password_button.setStyleSheet(self.show_button_style())
        self.show_password_button.toggled.connect(self.toggle_password_visibility)
        
        password_field_layout.addWidget(self.password_input, 1) 
        password_field_layout.addWidget(self.show_password_button)
        
        self.password_input.focusInEvent = lambda e, pc=self.password_container: self.set_focus_style(pc, True)
        self.password_input.focusOutEvent = lambda e, pc=self.password_container: self.set_focus_style(pc, False)
        scroll_layout.addWidget(self.password_container)
        
        confirm_label = QLabel("Confirm Password")
        confirm_label.setFont(QFont("Inter", 11))
        confirm_label.setStyleSheet("color: #000000;")
        scroll_layout.addWidget(confirm_label)

        self.confirm_container = QWidget()
        self.confirm_container.setFixedHeight(50)
        self.confirm_container.setStyleSheet(self.password_container_style(focused=False))
        confirm_field_layout = QHBoxLayout(self.confirm_container)
        confirm_field_layout.setContentsMargins(12, 0, 5, 0)
        confirm_field_layout.setSpacing(5)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setFont(QFont("Inter", 11))
        self.confirm_input.setStyleSheet("border: none; background: transparent;")

        self.show_confirm_button = QPushButton("Show")
        self.show_confirm_button.setFont(QFont("Inter", 10))
        self.show_confirm_button.setCheckable(True)
        self.show_confirm_button.setStyleSheet(self.show_button_style())
        self.show_confirm_button.toggled.connect(self.toggle_confirm_visibility)
        
        confirm_field_layout.addWidget(self.confirm_input, 1) 
        confirm_field_layout.addWidget(self.show_confirm_button)
        
        self.confirm_input.focusInEvent = lambda e, pc=self.confirm_container: self.set_focus_style(pc, True)
        self.confirm_input.focusOutEvent = lambda e, pc=self.confirm_container: self.set_focus_style(pc, False)
        scroll_layout.addWidget(self.confirm_container)

        scroll_layout.addSpacing(10)
        
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setFont(QFont("Inter", 12, QFont.Bold))
        self.signup_btn.setCursor(Qt.PointingHandCursor)
        self.signup_btn.setStyleSheet("""
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
        self.signup_btn.clicked.connect(self.handle_signup)
        scroll_layout.addWidget(self.signup_btn)
        
        scroll_layout.addSpacing(10)

        signin_layout = QHBoxLayout()
        signin_layout.addStretch()
        signin_label = QLabel("Already have an account?")
        signin_label.setFont(QFont("Inter", 10))
        signin_label.setStyleSheet("color: #333333;")
        signin_layout.addWidget(signin_label)
        
        self.signin_btn = QPushButton("Sign In")
        self.signin_btn.setFont(QFont("Inter", 10, QFont.Bold))
        self.signin_btn.setCursor(Qt.PointingHandCursor)
        self.signin_btn.setStyleSheet("""
            QPushButton {
                color: #00BFFF;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.signin_btn.clicked.connect(self.show_login)
        signin_layout.addWidget(self.signin_btn)
        signin_layout.addStretch()
        scroll_layout.addLayout(signin_layout)
        
        scroll_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.resizeEvent(None)

    def input_style(self):
        arrow_svg_base64 = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgZmlsbD0iIzAwQkZGRiIgdmlld0JveD0iMCAwIDE2IDE2Ij48cGF0aCBkPSJNNy4yNDcgMTEuMTQgMi40NTEgNi4zNDZhLjUuNSAwIDAgMSAuNzA4LS43MDhMOCA5LjI5M2w0Ljg0LTQuNjU0YS41LjUgMCAwIDEgLjcwOC43MDhMOC43MDcgMTEuMTRhLjUuNSAwIDAgMS0uNzA4IDB6Ii8+PC9zdmc+"
        
        style_part_1 = f"""
            QLineEdit, QDateEdit, QComboBox {{
                padding: 12px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
                color: #000000;
            }}
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {{
                border-color: #00BFFF;
            }}
            QDateEdit::drop-down, QComboBox::drop-down {{
                border: 0px;
                padding-right: 10px;
            }}
            QDateEdit::down-arrow, QComboBox::down-arrow {{
                image: url({arrow_svg_base64});
                width: 16px;
                height: 16px;
            }}
        """
        
        style_part_2 = """
            QDateEdit::down-arrow:on {
            }
            
            QComboBox QAbstractItemView {
                border: 2px solid #00BFFF;
                border-radius: 8px;
                background-color: white;
                color: #000000;
                selection-background-color: #e0f5ff;
                selection-color: #000000;
                padding: 5px;
            }
        """
        
        return style_part_1 + style_part_2

    def password_container_style(self, focused=False):
        border_color = "#00BFFF" if focused else "#e5e7eb"
        
        return """
            QWidget {{
                border: 2px solid {0};
                border-radius: 8px;
                background-color: white;
            }}
        """.format(border_color)
    
    def show_button_style(self):
        return """
            QPushButton {
                color: #00BFFF; 
                border: none; 
                background: transparent;
                padding-right: 5px;
            }
        """

    def set_focus_style(self, widget, has_focus):
        widget.setStyleSheet(self.password_container_style(focused=has_focus))

    def create_blurred_label(self, text, font_size):
        label = QLabel(text)
        label.setFont(QFont("Inter", font_size))
        label.setStyleSheet("color: rgba(0, 191, 255, 0.5); background: transparent;") 
        
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(1) 
        label.setGraphicsEffect(blur_effect)
        
        return label

    def resizeEvent(self, event):
        if not hasattr(self, 'top_bar_widget'):
            if event:
                super().resizeEvent(event)
            return

        w = self.width()
        h = self.height()
        
        self.top_bar_widget.setGeometry(30, 5, w - 60, 110)

        form_w = self.signup_form_widget.maximumWidth()
        
        form_h_float = h * 0.85
        if form_h_float < 750: 
            form_h = 750
        else:
            form_h = int(form_h_float)
        
        form_x = (w - form_w) // 2
        form_y = (h - form_h) // 2
        if form_y < 60: form_y = 60
        
        self.signup_form_widget.setGeometry(form_x, form_y, form_w, form_h)

        scale_x = w / self.BASE_WIDTH
        scale_y = h / self.BASE_HEIGHT
        
        for i, label in enumerate(self.diagram_labels):
            data = self.diagram_data[i]
            orig_pos = data["pos"]
            
            new_x = int(orig_pos[0] * scale_x)
            new_y = int(orig_pos[1] * scale_y)
            
            label.move(new_x, new_y)
        
        self.signup_form_widget.raise_()
        self.top_bar_widget.raise_()
        
        if event:
            super().resizeEvent(event)

    def toggle_password_visibility(self, toggled): 
        if toggled:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Show")

    def toggle_confirm_visibility(self, toggled): 
        if toggled:
            self.confirm_input.setEchoMode(QLineEdit.Normal)
            self.show_confirm_button.setText("Hide")
        else:
            self.confirm_input.setEchoMode(QLineEdit.Password)
            self.show_confirm_button.setText("Show")

    def handle_signup(self):
        full_name = self.fullname_input.text()
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_input.text()
        date_of_birth = self.dob_input.date().toString("yyyy-MM-dd")
        gender = self.gender_combo.currentText()
        
        if not all([full_name, username, email, password, confirm_password]):
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        if gender == "Select gender":
            QMessageBox.warning(self, "Error", "Please select a gender")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return
        
        print(f"UI: Calling API to register {username} / {email}")
        response = api_client.register(full_name, username, email, password, date_of_birth, gender)
        
        if "error" in response:
            QMessageBox.critical(self, "Registration Failed", response["error"])
        elif "requires_otp" in response and response["requires_otp"]:
            print(f"UI: OTP required for {response['email']}")
            otp_dialog = OTPDialog(response["email"], api_client, self)
            if otp_dialog.exec_():
                QMessageBox.information(self, "Success", "Account created and verified successfully!")
                self.show_login()
            else:
                print("UI: OTP dialog was cancelled or failed.")
                QMessageBox.warning(self, "OTP Failed", "Account created, but OTP verification failed. Please try logging in to re-verify.")
                self.show_login()
        else:
            QMessageBox.critical(self, "Error", "Invalid response from server")
    
    def show_login(self):
        from ui.login_window import LoginWindow 
        
        print("UI: Closing signup and opening login.")
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()