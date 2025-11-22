import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, 
    QDateEdit, QComboBox, QScrollArea, QFrame, QMenu, QAction, QDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QCursor
from api.django_client import api_client
from ui.error_dialog import ErrorDialog


class ProfileWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profile - Chemizer Analytics")
        self.setGeometry(100, 100, 1000, 800)
        self.showMaximized()
        self.setStyleSheet("background-color: #f3f4f6;")
        
        self.editing_mode = False
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.setup_navbar()
        layout.addWidget(self.navbar_widget)
        
        self.setup_profile_content()
        layout.addWidget(self.scroll_area)
        
        central_widget.setLayout(layout)
        
        self.load_user_profile()
        self.load_profile()
    
    def setup_navbar(self):
        from PyQt5.QtGui import QColor
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        
        self.navbar_widget = QFrame(self.centralWidget())
        
        self.navbar_widget.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border: none;
                border-bottom: 2px solid rgba(200, 200, 200, 0.4);
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.navbar_widget.setGraphicsEffect(shadow)
        
        navbar_layout = QHBoxLayout(self.navbar_widget)
        navbar_layout.setContentsMargins(50, 20, 50, 20)
        navbar_layout.setSpacing(40)
        
        brand_text = QLabel("Chemizer Analytics")
        brand_text.setFont(QFont("Comic Sans MS", 31, QFont.Bold))
        brand_text.setStyleSheet("color: #1f2937; border: none;")
        navbar_layout.addWidget(brand_text)
        
        navbar_layout.addStretch()
        
        self.upload_nav_btn = self.create_nav_button("📤 Upload", False)
        self.upload_nav_btn.clicked.connect(self.show_upload)
        navbar_layout.addWidget(self.upload_nav_btn)
        
        self.dashboard_nav_btn = self.create_nav_button("📊 Dashboard", False)
        self.dashboard_nav_btn.clicked.connect(self.show_dashboard)
        navbar_layout.addWidget(self.dashboard_nav_btn)
        
        self.history_nav_btn = self.create_nav_button("📜 History", False)
        self.history_nav_btn.clicked.connect(self.show_history)
        navbar_layout.addWidget(self.history_nav_btn)
        
        self.profile_btn = QPushButton("👤 Profile ")
        self.profile_btn.setFont(QFont("Segoe UI", 17, QFont.Bold))
        self.profile_btn.setCursor(Qt.PointingHandCursor)
        self.profile_btn.setMinimumWidth(250)
        self.profile_btn.setStyleSheet("""
            QPushButton {
                padding: 16px 26px;
                background-color: rgba(31, 41, 55, 0.05);
                color: #1f2937;
                border: 2px solid rgba(31, 41, 55, 0.1);
                border-radius: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(31, 41, 55, 0.1);
                border-color: #1f2937;
            }
        """)
        
        profile_menu = QMenu(self)
        profile_menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 2px solid rgba(200, 200, 200, 0.8);
                border-radius: 16px;
                padding: 12px;
                min-width: 280px;
            }
            QMenu::item {
                color: #1f2937;
                padding: 18px 32px;
                border-radius: 10px;
                margin: 4px 0px;
                font-size: 18px;
                font-weight: 600;
            }
            QMenu::item:selected {
                background-color: rgba(0, 191, 255, 0.15);
                color: #00BFFF;
            }
            QMenu::separator {
                height: 2px;
                background-color: rgba(200, 200, 200, 0.5);
                margin: 10px 16px;
            }
        """)
        
        view_profile_action = QAction("👤  My Profile", self)
        view_profile_action.setFont(QFont("Segoe UI", 17))
        profile_menu.addAction(view_profile_action)
        
        settings_action = QAction("⚙️  Settings", self)
        settings_action.setFont(QFont("Segoe UI", 17))
        settings_action.triggered.connect(self.show_settings)
        profile_menu.addAction(settings_action)
        
        profile_menu.addSeparator()
        
        logout_action = QAction("🚪  Logout", self)
        logout_action.setFont(QFont("Segoe UI", 17))
        logout_action.triggered.connect(self.logout)
        profile_menu.addAction(logout_action)
        
        self.profile_btn.setMenu(profile_menu)
        navbar_layout.addWidget(self.profile_btn)
        
        self.navbar_widget.setFixedHeight(120)
    
    def create_nav_button(self, text, active=False):
        btn = QPushButton(text)
        btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumWidth(180)
        
        if active:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 16px 26px;
                    background-color: #1f2937;
                    color: white;
                    border: none;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: #374151;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 16px 26px;
                    background-color: transparent;
                    color: #1f2937;
                    border: none;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: rgba(31, 41, 55, 0.08);
                }
            """)
        
        return btn
    
    def load_user_profile(self):
        response = api_client.get_profile()
        
        if "error" not in response:
            username = response.get("username", "User")
            full_name = response.get("full_name", username)
            display_name = full_name.split()[0] if full_name else username
            self.profile_btn.setText(f"👤 {display_name} ")
    
    def setup_profile_content(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: #f3f4f6;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #f3f4f6;")
        self.scroll_area.setWidget(scroll_content)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 50)
        layout.setSpacing(25)
        
        title = QLabel("My Profile")
        title.setFont(QFont("Comic Sans MS", 40, QFont.Bold))
        title.setStyleSheet("color: #000000; background: transparent;")
        layout.addWidget(title)
        
        subtitle = QLabel("Manage your account information")
        subtitle.setFont(QFont("Inter", 16))
        subtitle.setStyleSheet("color: #666666; background: transparent;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        picture_frame = QFrame()
        picture_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 32px;
            }
        """)
        picture_layout = QHBoxLayout(picture_frame)
        picture_layout.setSpacing(30)
        
        avatar_label = QLabel("👤")
        avatar_label.setFont(QFont("Segoe UI", 90))
        avatar_label.setFixedSize(100, 100)
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setStyleSheet("""
            QLabel {
                background-color: #e0f5ff;
                border-radius: 80px;
            }
        """)
        picture_layout.addWidget(avatar_label)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        self.profile_name_label = QLabel("Loading...")
        self.profile_name_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.profile_name_label.setStyleSheet("background: transparent; color: #1f2937;")
        info_layout.addWidget(self.profile_name_label)
        
        username_container = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        username_label.setStyleSheet("color: #666666; background: transparent;")
        self.username_display = QLabel("Loading...")
        self.username_display.setFont(QFont("Segoe UI", 18))
        self.username_display.setStyleSheet("color: #1f2937; background: transparent;")
        username_container.addWidget(username_label)
        username_container.addWidget(self.username_display)
        username_container.addStretch()
        info_layout.addLayout(username_container)
        
        email_container = QHBoxLayout()
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        email_label.setStyleSheet("color: #666666; background: transparent;")
        self.email_display = QLabel("Loading...")
        self.email_display.setFont(QFont("Segoe UI", 18))
        self.email_display.setStyleSheet("color: #1f2937; background: transparent;")
        email_container.addWidget(email_label)
        email_container.addWidget(self.email_display)
        email_container.addStretch()
        info_layout.addLayout(email_container)
        
        self.profile_member_label = QLabel("Member since: Loading...")
        self.profile_member_label.setFont(QFont("Segoe UI", 16))
        self.profile_member_label.setStyleSheet("color: #9ca3af; background: transparent;")
        info_layout.addWidget(self.profile_member_label)
        
        info_layout.addStretch()
        picture_layout.addLayout(info_layout)
        picture_layout.addStretch()
        
        layout.addWidget(picture_frame)
        
        layout.addSpacing(30)
        
        info_section_label = QLabel("Personal Information")
        info_section_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        info_section_label.setStyleSheet("color: #1f2937; background: transparent;")
        layout.addWidget(info_section_label)
        
        layout.addSpacing(20)
        
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        name_label = QLabel("Full Name")
        name_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        name_label.setStyleSheet("color: #374151; background: transparent;")
        form_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Segoe UI", 18))
        self.name_input.setReadOnly(True)
        self.name_input.setFixedHeight(55)
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 14px 18px;
                border: none;
                border-radius: 8px;
                background-color: #f9fafb;
                color: #6b7280;
                font-size: 18px;
            }
            QLineEdit:focus {
                background-color: #ffffff;
                color: #1f2937;
            }
        """)
        form_layout.addWidget(self.name_input)
        
        dob_label = QLabel("Date of Birth")
        dob_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        dob_label.setStyleSheet("color: #374151; background: transparent;")
        form_layout.addWidget(dob_label)
        
        self.dob_input = QDateEdit()
        self.dob_input.setDate(QDate(2000, 1, 1))
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setFont(QFont("Segoe UI", 18))
        self.dob_input.setReadOnly(True)
        self.dob_input.setFixedHeight(55)
        self.dob_input.setStyleSheet("""
            QDateEdit {
                padding: 14px 18px;
                border: none;
                border-radius: 8px;
                background-color: #f9fafb;
                color: #6b7280;
                font-size: 18px;
            }
            QDateEdit:focus {
                background-color: #ffffff;
                color: #1f2937;
            }
        """)
        form_layout.addWidget(self.dob_input)
        
        gender_label = QLabel("Gender")
        gender_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        gender_label.setStyleSheet("color: #374151; background: transparent;")
        form_layout.addWidget(gender_label)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other", "Prefer not to say"])
        self.gender_combo.setFont(QFont("Segoe UI", 18))
        self.gender_combo.setEnabled(False)
        self.gender_combo.setFixedHeight(55)
        self.gender_combo.setStyleSheet("""
            QComboBox {
                padding: 14px 18px;
                border: none;
                border-radius: 8px;
                background-color: #f9fafb;
                color: #6b7280;
                font-size: 18px;
            }
            QComboBox:focus {
                background-color: #ffffff;
                color: #1f2937;
            }
        """)
        form_layout.addWidget(self.gender_combo)
        
        form_layout.addStretch()
        layout.addWidget(form_container)
        
        layout.addSpacing(30)
        
        button_container = QHBoxLayout()
        button_container.setSpacing(15)
        
        self.edit_btn = QPushButton("✏️  Edit Profile")
        self.edit_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.setMinimumHeight(75)
        self.edit_btn.setMinimumWidth(220)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                padding: 14px 40px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        self.edit_btn.clicked.connect(self.enable_editing)
        button_container.addWidget(self.edit_btn)
        
        self.save_btn = QPushButton("💾 Save Changes")
        self.save_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setMinimumHeight(75)
        self.save_btn.setMinimumWidth(240)
        self.save_btn.setStyleSheet("""
            QPushButton {
                padding: 14px 40px;
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        self.save_btn.clicked.connect(self.save_profile)
        self.save_btn.hide()
        button_container.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("✕ Cancel")
        self.cancel_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setMinimumHeight(75)
        self.cancel_btn.setMinimumWidth(180)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 14px 40px;
                background-color: #6b7280;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        self.cancel_btn.clicked.connect(self.disable_editing)
        self.cancel_btn.hide()
        button_container.addWidget(self.cancel_btn)
        
        button_container.addStretch()
        layout.addLayout(button_container)
        
        layout.addSpacing(30)
        
        action_button_layout = QHBoxLayout()
        action_button_layout.setSpacing(15)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setMinimumHeight(80)
        logout_btn.setMinimumWidth(200)
        logout_btn.setStyleSheet("""
            QPushButton {
                padding: 14px 40px;
                background-color: #6b7280;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        action_button_layout.addWidget(logout_btn)
        
        delete_btn = QPushButton("Delete Account")
        delete_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setMinimumHeight(80)
        delete_btn.setMinimumWidth(260)
        delete_btn.setStyleSheet("""
            QPushButton {
                padding: 14px 40px;
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        delete_btn.clicked.connect(self.delete_account)
        action_button_layout.addWidget(delete_btn)
        
        action_button_layout.addStretch()
        layout.addLayout(action_button_layout)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
    
    def enable_editing(self):
        self.editing_mode = True
        self.name_input.setReadOnly(False)
        self.dob_input.setReadOnly(False)
        self.gender_combo.setEnabled(True)
        
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 14px 18px;
                border: 2px solid #2563eb;
                border-radius: 8px;
                background-color: #ffffff;
                color: #1f2937;
                font-size: 18px;
            }
            QLineEdit:focus {
                border: 2px solid #1d4ed8;
            }
        """)
        
        self.dob_input.setStyleSheet("""
            QDateEdit {
                padding: 14px 18px;
                border: 2px solid #2563eb;
                border-radius: 8px;
                background-color: #ffffff;
                color: #1f2937;
                font-size: 18px;
            }
            QDateEdit:focus {
                border: 2px solid #1d4ed8;
            }
        """)
        
        self.gender_combo.setStyleSheet("""
            QComboBox {
                padding: 14px 18px;
                border: 2px solid #2563eb;
                border-radius: 8px;
                background-color: #ffffff;
                color: #1f2937;
                font-size: 18px;
            }
            QComboBox:focus {
                border: 2px solid #1d4ed8;
            }
        """)
        
        self.edit_btn.hide()
        self.save_btn.show()
        self.cancel_btn.show()
    
    def disable_editing(self):
        self.editing_mode = False
        self.load_profile()
        
        self.name_input.setReadOnly(True)
        self.dob_input.setReadOnly(True)
        self.gender_combo.setEnabled(False)
        
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 14px 18px;
                border: none;
                border-radius: 8px;
                background-color: #f9fafb;
                color: #6b7280;
                font-size: 18px;
            }
            QLineEdit:focus {
                background-color: #ffffff;
                color: #1f2937;
            }
        """)
        
        self.dob_input.setStyleSheet("""
            QDateEdit {
                padding: 14px 18px;
                border: none;
                border-radius: 8px;
                background-color: #f9fafb;
                color: #6b7280;
                font-size: 18px;
            }
            QDateEdit:focus {
                background-color: #ffffff;
                color: #1f2937;
            }
        """)
        
        self.gender_combo.setStyleSheet("""
            QComboBox {
                padding: 14px 18px;
                border: none;
                border-radius: 8px;
                background-color: #f9fafb;
                color: #6b7280;
                font-size: 18px;
            }
            QComboBox:focus {
                background-color: #ffffff;
                color: #1f2937;
            }
        """)
        
        self.edit_btn.show()
        self.save_btn.hide()
        self.cancel_btn.hide()
    
    def load_profile(self):
        response = api_client.get_profile()
        
        if "error" in response:
            error_dialog = ErrorDialog("Error", f"Failed to load profile: {response['error']}", self)
            error_dialog.exec_()
            return
        
        full_name = response.get("full_name", "")
        username = response.get("username", "")
        email = response.get("email", "")
        
        self.profile_name_label.setText(full_name or "Not Set")
        self.username_display.setText(username or "Not Set")
        self.email_display.setText(email or "Not Set")
        
        created_at = response.get("created_at", "")
        if created_at:
            try:
                from datetime import datetime
                date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                member_since = date_obj.strftime("%b %Y")
                self.profile_member_label.setText(f"Member since: {member_since}")
            except:
                self.profile_member_label.setText("Member since: Unknown")
        else:
            self.profile_member_label.setText("Member since: Unknown")
        
        self.name_input.setText(full_name or "")
        
        dob_str = response.get("date_of_birth")
        if dob_str:
            try:
                dob_date = QDate.fromString(dob_str, "yyyy-MM-dd")
                if dob_date.isValid():
                    self.dob_input.setDate(dob_date)
            except:
                pass
        
        gender = response.get("gender", "Male")
        index = self.gender_combo.findText(gender, Qt.MatchFixedString)
        if index >= 0:
            self.gender_combo.setCurrentIndex(index)
    
    def save_profile(self):
        profile_data = {
            "full_name": self.name_input.text(),
            "date_of_birth": self.dob_input.date().toString("yyyy-MM-dd"),
            "gender": self.gender_combo.currentText()
        }
        
        response = api_client.update_profile(profile_data)
        
        if "error" in response:
            from ui.custom_dialogs import LargeErrorDialog
            error_dialog = LargeErrorDialog("Error", response["error"], self)
            error_dialog.exec_()
        else:
            from ui.custom_dialogs import LargeSuccessDialog
            success_dialog = LargeSuccessDialog("Success!", "Profile updated successfully!", self)
            success_dialog.exec_()
            
            full_name = self.name_input.text()
            display_name = full_name.split()[0] if full_name else "User"
            self.profile_btn.setText(f"👤 {display_name} ")
            
            self.profile_name_label.setText(full_name)
            self.disable_editing()
    
    def delete_account(self):
        from ui.custom_dialogs import CompactConfirmDialog
        
        dialog = CompactConfirmDialog(
            "Delete Account?",
            "⚠️ Are you sure you want to delete your account?\n\n"
            "• Your profile information\n"
            "• All uploaded files\n"
            "• All analysis data\n"
            "• All generated reports",
            self
        )
        
        if dialog.exec_() == QDialog.Accepted:
            response = api_client.delete_account()
            if "error" in response:
                from ui.custom_dialogs import CompactErrorDialog
                error_dialog = CompactErrorDialog("Error", response["error"], self)
                error_dialog.exec_()
            else:
                from ui.custom_dialogs import CompactSuccessDialog
                success_dialog = CompactSuccessDialog("Success!", "Account deleted successfully!", self)
                success_dialog.exec_()
                
                api_client.set_token(None)
                
                from ui.login_window import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()
                self.close()
    
    def show_upload(self):
        from ui.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
    
    def show_dashboard(self):
        from ui.dashboard_window import DashboardWindow
        self.dashboard_window = DashboardWindow()
        self.dashboard_window.show()
        self.close()
    
    def show_history(self):
        from ui.history_window import HistoryWindow
        self.history_window = HistoryWindow()
        self.history_window.show()
        self.close()
    
    def show_settings(self):
        from ui.settings_window import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()
    
    def logout(self):
        from ui.custom_dialogs import CompactConfirmDialog
        
        dialog = CompactConfirmDialog(
            "Logout?",
            "Are you sure you want to logout?\n\nYou will need to login again to access your account.",
            self
        )
        
        if dialog.exec_() == QDialog.Accepted:
            api_client.set_token(None)
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()