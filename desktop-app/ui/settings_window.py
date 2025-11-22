import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QFrame, QScrollArea,
    QGraphicsDropShadowEffect, QMenu, QAction, QDialog,
    QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from api.django_client import api_client
from ui.error_dialog import ErrorDialog


class DownloadAllThread(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            import csv
            import os
            from datetime import datetime
            
            response = api_client.get_upload_history()
            if "error" in response:
                self.finished.emit(False, response["error"])
                return
            
            uploads = response.get("uploads", [])
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"chemizer_data_export_{timestamp}.csv"
            desktop_path = os.path.expanduser("~/Desktop")
            csv_path = os.path.join(desktop_path, csv_filename)
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Upload ID', 'Filename', 'Status', 'Rows', 'File Size (KB)', 'Upload Date', 'Analysis Date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for upload in uploads:
                    writer.writerow({
                        'Upload ID': upload.get('upload_id', ''),
                        'Filename': upload.get('filename', ''),
                        'Status': upload.get('status', ''),
                        'Rows': upload.get('rows', ''),
                        'File Size (KB)': upload.get('file_size', 0) / 1024,
                        'Upload Date': upload.get('upload_date_formatted', ''),
                        'Analysis Date': upload.get('analysis_date_formatted', '')
                    })
            
            self.finished.emit(True, f"Data exported to: {csv_path}")
        except Exception as e:
            self.finished.emit(False, str(e))


class DeleteAllThread(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            response = api_client.get_upload_history()
            if "error" in response:
                self.finished.emit(False, response["error"])
                return
            
            uploads = response.get("uploads", [])
            
            for upload in uploads:
                upload_id = upload.get("upload_id")
                api_client.delete_upload(upload_id)
            
            self.finished.emit(True, f"Successfully deleted {len(uploads)} uploads!")
        except Exception as e:
            self.finished.emit(False, str(e))


class ChangePasswordDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Change Password")
        self.setModal(True)
        self.setFixedSize(520, 480)
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 520) // 2
            y = parent_geo.y() + (parent_geo.height() - 480) // 2
            self.move(x, y)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)
        
        title = QLabel("🔐 Change Password")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        info_label = QLabel("Enter your current and new password")
        info_label.setFont(QFont("Segoe UI", 13))
        info_label.setStyleSheet("color: #6b7280; background: transparent;")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addSpacing(15)
        
        current_pwd_label = QLabel("Current Password:")
        current_pwd_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        current_pwd_label.setStyleSheet("color: #1f2937; background: transparent;")
        layout.addWidget(current_pwd_label)
        
        self.current_password_input = QLineEdit()
        self.current_password_input.setPlaceholderText("Enter current password")
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setFont(QFont("Segoe UI", 11))
        self.current_password_input.setFixedHeight(45)
        self.current_password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
        """)
        layout.addWidget(self.current_password_input)
        
        new_pwd_label = QLabel("New Password:")
        new_pwd_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        new_pwd_label.setStyleSheet("color: #1f2937; background: transparent;")
        layout.addWidget(new_pwd_label)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setFont(QFont("Segoe UI", 11))
        self.new_password_input.setFixedHeight(45)
        self.new_password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
        """)
        layout.addWidget(self.new_password_input)
        
        confirm_pwd_label = QLabel("Confirm New Password:")
        confirm_pwd_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        confirm_pwd_label.setStyleSheet("color: #1f2937; background: transparent;")
        layout.addWidget(confirm_pwd_label)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setFont(QFont("Segoe UI", 11))
        self.confirm_password_input.setFixedHeight(45)
        self.confirm_password_input.setStyleSheet(self.new_password_input.styleSheet())
        layout.addWidget(self.confirm_password_input)
        
        layout.addSpacing(15)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFixedHeight(50)
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 28px;
                background-color: #6b7280;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Save Password")
        save_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setFixedHeight(50)
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 28px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        save_btn.clicked.connect(self.save_password)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
                border: 2px solid #e5e7eb;
            }
        """)
    
    def save_password(self):
        current_pwd = self.current_password_input.text()
        new_pwd = self.new_password_input.text()
        confirm_pwd = self.confirm_password_input.text()
        
        if not current_pwd:
            try:
                from ui.custom_dialogs import CompactErrorDialog
                dialog = CompactErrorDialog("Error", "Please enter your current password", self)
                dialog.exec_()
            except ImportError:
                QMessageBox.warning(self, "Error", "Please enter your current password")
            return
        
        if not new_pwd or not confirm_pwd:
            try:
                from ui.custom_dialogs import CompactErrorDialog
                dialog = CompactErrorDialog("Error", "Please fill in all password fields", self)
                dialog.exec_()
            except ImportError:
                QMessageBox.warning(self, "Error", "Please fill in all password fields")
            return
        
        if new_pwd != confirm_pwd:
            try:
                from ui.custom_dialogs import CompactErrorDialog
                dialog = CompactErrorDialog("Error", "New passwords do not match!", self)
                dialog.exec_()
            except ImportError:
                QMessageBox.warning(self, "Error", "New passwords do not match!")
            return
        
        if len(new_pwd) < 8:
            try:
                from ui.custom_dialogs import CompactErrorDialog
                dialog = CompactErrorDialog("Error", "Password must be at least 8 characters", self)
                dialog.exec_()
            except ImportError:
                QMessageBox.warning(self, "Error", "Password must be at least 8 characters")
            return
        
        response = api_client.change_password(current_pwd, new_pwd)
        
        if "error" in response:
            try:
                from ui.custom_dialogs import CompactErrorDialog
                dialog = CompactErrorDialog("Error", response["error"], self)
                dialog.exec_()
            except ImportError:
                QMessageBox.warning(self, "Error", response["error"])
        else:
            try:
                from ui.custom_dialogs import CompactSuccessDialog
                dialog = CompactSuccessDialog(
                    "Success!",
                    "Your password has been changed successfully!",
                    self
                )
                dialog.exec_()
            except ImportError:
                QMessageBox.information(self, "Success!", "Your password has been changed successfully!")
            
            self.accept()


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings - Chemizer Analytics")
        self.setGeometry(100, 100, 1200, 800)
        
        self.showMaximized()
        
        self.setStyleSheet("background-color: #f3f4f6;")
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f3f4f6;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.setup_navbar()
        layout.addWidget(self.navbar_widget)
        
        self.setup_settings_content()
        layout.addWidget(self.settings_scroll_area)
        
        central_widget.setLayout(layout)
        
        self.load_user_profile()
        
        self.load_settings_data()
    
    def setup_navbar(self):
        self.navbar_widget = QFrame()
        
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
        self.profile_btn.setMinimumWidth(240)
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
        view_profile_action.triggered.connect(self.show_profile)
        profile_menu.addAction(view_profile_action)
        
        settings_action = QAction("⚙️  Settings", self)
        settings_action.setFont(QFont("Segoe UI", 17))
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
        else:
            self.profile_btn.setText("👤 User ")
    
    def setup_settings_content(self):
        self.settings_scroll_area = QScrollArea()
        self.settings_scroll_area.setWidgetResizable(True)
        self.settings_scroll_area.setStyleSheet("border: none; background-color: #f3f4f6;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #f3f4f6;")
        self.settings_scroll_area.setWidget(scroll_content)
        
        main_layout = QHBoxLayout(scroll_content)
        main_layout.addStretch()
        
        content_container = QWidget()
        content_container.setMaximumWidth(900)
        content_container.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(content_container)
        layout.setContentsMargins(30, 30, 30, 50)
        layout.setSpacing(30)
        
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Comic Sans MS", 36, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent;")
        layout.addWidget(title)
        
        subtitle = QLabel("Manage your preferences and account")
        subtitle.setFont(QFont("Inter", 15))
        subtitle.setStyleSheet("color: #666666; background: transparent;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        self.add_section(layout, "👤 Account Information")
        
        account_frame = self.create_frame()
        account_layout = QVBoxLayout(account_frame)
        account_layout.setSpacing(18)
        
        self.username_label = QLabel("Username: Loading...")
        self.username_label.setFont(QFont("Inter", 16))
        self.username_label.setStyleSheet("color: #1f2937; background: transparent;")
        account_layout.addWidget(self.username_label)
        
        self.email_label = QLabel("Email: Loading...")
        self.email_label.setFont(QFont("Inter", 16))
        self.email_label.setStyleSheet("color: #1f2937; background: transparent;")
        account_layout.addWidget(self.email_label)
        
        self.verified_label = QLabel("✅ Account verified on: Loading...")
        self.verified_label.setFont(QFont("Inter", 14))
        self.verified_label.setStyleSheet("color: #059669; background: transparent;")
        account_layout.addWidget(self.verified_label)
        
        self.last_login_label = QLabel("🖥️ Last login: Loading...")
        self.last_login_label.setFont(QFont("Inter", 14))
        self.last_login_label.setStyleSheet("color: #6b7280; background: transparent;")
        account_layout.addWidget(self.last_login_label)
        
        change_pwd_btn = QPushButton("🔐 Change Password")
        change_pwd_btn.setFont(QFont("Inter", 16, QFont.Bold))
        change_pwd_btn.setCursor(Qt.PointingHandCursor)
        change_pwd_btn.setMinimumHeight(75)
        change_pwd_btn.setStyleSheet("""
            QPushButton {
                padding: 14px 28px;
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
        change_pwd_btn.clicked.connect(self.change_password)
        account_layout.addWidget(change_pwd_btn)
        
        layout.addWidget(account_frame)
        
        self.add_section(layout, "📊 Data Management")
        
        data_frame = self.create_frame()
        data_layout = QVBoxLayout(data_frame)
        data_layout.setSpacing(18)
        
        self.storage_label = QLabel("📦 Total data uploaded: Loading...")
        self.storage_label.setFont(QFont("Inter", 16, QFont.Bold))
        self.storage_label.setStyleSheet("color: #1f2937; background: transparent;")
        data_layout.addWidget(self.storage_label)
        
        self.upload_count_label = QLabel("📤 Total uploads: Loading...")
        self.upload_count_label.setFont(QFont("Inter", 16, QFont.Bold))
        self.upload_count_label.setStyleSheet("color: #1f2937; background: transparent;")
        data_layout.addWidget(self.upload_count_label)
        
        data_layout.addSpacing(10)
        
        delete_all_btn = QPushButton("🗑️ Delete All Uploads")
        delete_all_btn.setFont(QFont("Inter", 16, QFont.Bold))
        delete_all_btn.setCursor(Qt.PointingHandCursor)
        delete_all_btn.setMinimumHeight(75)
        delete_all_btn.setStyleSheet("""
            QPushButton {
                padding: 14px 28px;
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
        delete_all_btn.clicked.connect(self.delete_all_uploads)
        data_layout.addWidget(delete_all_btn)
        
        layout.addWidget(data_frame)
        
        layout.addStretch()
        
        main_layout.addWidget(content_container)
        main_layout.addStretch()
    
    def add_section(self, parent_layout, title):
        label = QLabel(title)
        label.setFont(QFont("Inter", 22, QFont.Bold))
        label.setStyleSheet("color: #1f2937; background: transparent; margin-top: 10px;")
        parent_layout.addWidget(label)
    
    def create_frame(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #2563eb;
                border-radius: 16px;
                padding: 25px;
            }
        """)
        return frame
    
    def load_settings_data(self):
        profile = api_client.get_profile()
        if "error" not in profile:
            username = profile.get("username", "N/A")
            email = profile.get("email", "N/A")
            created_at = profile.get("created_at", "")
            
            self.username_label.setText(f"Username: {username}")
            self.email_label.setText(f"Email: {email}")
            
            if created_at:
                try:
                    from datetime import datetime
                    date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    verified_date = date_obj.strftime("%B %d, %Y")
                    self.verified_label.setText(f"✅ Account verified on: {verified_date}")
                    self.last_login_label.setText(f"🖥️ Last login: {date_obj.strftime('%B %d, %Y at %I:%M %p')}")
                except:
                    self.verified_label.setText("✅ Account verified")
                    self.last_login_label.setText("🖥️ Last login: Recently")
        
        history = api_client.get_upload_history()
        if "error" not in history:
            uploads = history.get("uploads", [])
            total_uploads = len(uploads)
            
            total_size = sum(upload.get("file_size", 0) for upload in uploads)
            size_mb = total_size / (1024 * 1024)
            
            self.storage_label.setText(f"📦 Total data uploaded: {size_mb:.2f} MB")
            self.upload_count_label.setText(f"📤 Total uploads: {total_uploads} files")
        else:
            self.storage_label.setText("📦 Total data uploaded: 0 MB")
            self.upload_count_label.setText("📤 Total uploads: 0 files")
    
    def change_password(self):
        dialog = ChangePasswordDialog(self)
        dialog.exec_()
    
    def delete_all_uploads(self):
        try:
            from ui.custom_dialogs import CompactConfirmDialog
            
            dialog = CompactConfirmDialog(
                "Delete All Uploads?",
                "⚠️ This will permanently delete:\n"
                "• All uploaded files\n"
                "• All analysis data\n"
                "• All generated reports\n\n"
                "This action CANNOT be undone!",
                self
            )
            
            if dialog.exec_() == QDialog.Accepted:
                confirm2 = CompactConfirmDialog(
                    "Final Confirmation",
                    "This is your last chance!\n\n"
                    "Click Confirm to delete everything.",
                    self
                )
                
                if confirm2.exec_() == QDialog.Accepted:
                    self.delete_thread = DeleteAllThread()
                    self.delete_thread.finished.connect(self.delete_complete)
                    self.delete_thread.start()
        except ImportError:
            reply = QMessageBox.question(
                self,
                "Delete All Uploads?",
                "⚠️ This will permanently delete all data. Continue?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.delete_thread = DeleteAllThread()
                self.delete_thread.finished.connect(self.delete_complete)
                self.delete_thread.start()
    
    def delete_complete(self, success, message):
        if success:
            try:
                from ui.custom_dialogs import CompactSuccessDialog
                dialog = CompactSuccessDialog("Success!", message, self)
                dialog.exec_()
            except ImportError:
                QMessageBox.information(self, "Success!", message)
            self.load_settings_data()
        else:
            try:
                from ui.custom_dialogs import CompactErrorDialog
                dialog = CompactErrorDialog("Error", message, self)
                dialog.exec_()
            except ImportError:
                QMessageBox.warning(self, "Error", message)
    
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
    
    def show_profile(self):
        from ui.profile_window import ProfileWindow
        self.profile_window = ProfileWindow()
        self.profile_window.show()
        self.close()
    
    def logout(self):
        try:
            from ui.custom_dialogs import CompactConfirmDialog
            
            dialog = CompactConfirmDialog(
                "Logout?",
                "Are you sure you want to logout?\n\nYou will need to login again.",
                self
            )
            
            if dialog.exec_() == QDialog.Accepted:
                api_client.set_token(None)
                from ui.login_window import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()
                self.close()
        except ImportError:
            reply = QMessageBox.question(
                self,
                "Logout?",
                "Are you sure you want to logout?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                api_client.set_token(None)
                from ui.login_window import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()
                self.close()