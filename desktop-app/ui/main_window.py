import sys
import random
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QProgressBar, 
    QMessageBox, QGraphicsBlurEffect, QGraphicsDropShadowEffect,
    QSpacerItem, QSizePolicy, QFrame, QMenu, QAction
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPainter, QColor, QPalette
from api.django_client import api_client
from ui.results_window import ResultsWindow
from ui.dashboard_window import DashboardWindow
from ui.profile_window import ProfileWindow
from ui.history_window import HistoryWindow
from ui.settings_window import SettingsWindow
from ui.error_dialog import ErrorDialog


class UploadThread(QThread):
    progress = pyqtSignal(int)
    status_message = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        import time
        
        steps = [
            (10, "📂 Reading file..."),
            (30, "🔍 Analyzing data structure..."),
            (50, "📊 Processing columns..."),
            (70, "🎨 Generating visualizations..."),
            (90, "✨ Finalizing insights...")
        ]
        
        for progress, message in steps:
            self.progress.emit(progress)
            self.status_message.emit(message)
            time.sleep(0.5)
        
        result = api_client.upload_file(self.file_path)
        
        self.progress.emit(100)
        self.status_message.emit("✅ Analysis complete!")
        time.sleep(0.3)
        
        self.finished.emit(result)


class ClickableFrame(QFrame):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    BASE_WIDTH = 1200
    BASE_HEIGHT = 800

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Upload File - Chemizer Analytics")
        self.setGeometry(100, 100, self.BASE_WIDTH, self.BASE_HEIGHT)
        
        self.showMaximized()
        
        self.selected_file = None
        self.current_user = None

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #f3f4f6;")
        self.setCentralWidget(self.central_widget)
        
        self.setup_background_icons()
        
        self.setup_navbar()

        self.setup_upload_content()
        
        self.load_user_profile()
        
        self.resizeEvent(None)
    
    def setup_background_icons(self):
        self.diagram_data = [
            {"text": "H₂O", "font_size": 48, "pos": (50, 150)},
            {"text": "⚙️", "font_size": 54, "pos": (150, 300)},
            {"text": "📊", "font_size": 51, "pos": (250, 100)},
            {"text": "🔬", "font_size": 48, "pos": (100, 500)},
            {"text": "🧪", "font_size": 54, "pos": (300, 600)},
            {"text": "📈", "font_size": 51, "pos": (50, 650)},
            {"text": "⚗️", "font_size": 48, "pos": (950, 120)},
            {"text": "🌡️", "font_size": 54, "pos": (1050, 250)},
            {"text": "💧", "font_size": 51, "pos": (1100, 80)},
            {"text": "🔍", "font_size": 48, "pos": (1000, 400)},
            {"text": "📋", "font_size": 54, "pos": (1050, 620)},
            {"text": "⚡", "font_size": 51, "pos": (950, 500)},
        ]
        
        self.diagram_labels = []
        for data in self.diagram_data:
            label = self.create_blurred_label(data["text"], data["font_size"])
            label.setParent(self.central_widget)
            self.diagram_labels.append(label)

    def create_blurred_label(self, text, font_size):
        label = QLabel(text)
        label.setFont(QFont("Segoe UI Emoji", font_size))
        label.setStyleSheet("color: rgba(0, 191, 255, 0.3); background: transparent;")
        
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(2)
        label.setGraphicsEffect(blur_effect)
        
        return label
    
    def setup_navbar(self):
        self.navbar_widget = QFrame(self.central_widget)
        
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
        
        self.upload_nav_btn = self.create_nav_button("📤 Upload", True)
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
        settings_action.triggered.connect(self.show_settings)
        profile_menu.addAction(settings_action)
        
        profile_menu.addSeparator()
        
        logout_action = QAction("🚪  Logout", self)
        logout_action.setFont(QFont("Segoe UI", 17))
        logout_action.triggered.connect(self.logout)
        profile_menu.addAction(logout_action)
        
        self.profile_btn.setMenu(profile_menu)
        navbar_layout.addWidget(self.profile_btn)
    
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
    
    def setup_upload_content(self):
        self.upload_content_widget = QWidget(self.central_widget)
        self.upload_content_widget.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(self.upload_content_widget)
        layout.setContentsMargins(100, 30, 100, 60)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignTop)
        
        title = QLabel("Upload Your Data")
        title.setFont(QFont("Segoe UI", 48, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #111827; background: transparent;")
        layout.addWidget(title)
        
        subtitle = QLabel("Upload a CSV or Excel file for AI-powered analysis")
        subtitle.setFont(QFont("Segoe UI", 19))
        subtitle.setStyleSheet("color: #374151; background: transparent;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        self.upload_box = ClickableFrame()
        self.upload_box.setFixedSize(350, 350)
        self.upload_box.setStyleSheet("""
            ClickableFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border: 3px solid rgba(31, 41, 55, 0.2);
                border-radius: 28px;
            }
            ClickableFrame:hover {
                background-color: rgba(248, 250, 252, 1.0);
                border-color: rgba(31, 41, 55, 0.35);
            }
        """)
        
        self.upload_box.clicked.connect(self.choose_file)
        
        box_shadow = QGraphicsDropShadowEffect()
        box_shadow.setBlurRadius(30)
        box_shadow.setXOffset(0)
        box_shadow.setYOffset(6)
        box_shadow.setColor(QColor(0, 0, 0, 25))
        self.upload_box.setGraphicsEffect(box_shadow)
        
        box_layout = QVBoxLayout(self.upload_box)
        box_layout.setAlignment(Qt.AlignCenter)
        box_layout.setSpacing(18)
        box_layout.setContentsMargins(30, 30, 30, 30)
        
        self.file_label = QLabel("Click anywhere to select file")
        self.file_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("color: #6b7280;")
        self.file_label.setWordWrap(True)
        self.file_label.setMinimumHeight(50)
        box_layout.addWidget(self.file_label)
        
        box_layout.addSpacing(6)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: rgba(31, 41, 55, 0.12); max-height: 2px;")
        box_layout.addWidget(divider)
        
        box_layout.addSpacing(6)
        
        info_container = QVBoxLayout()
        info_container.setSpacing(8)
        
        format_label = QLabel("📄 Supported Formats")
        format_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        format_label.setStyleSheet("color: #1f2937;")
        info_container.addWidget(format_label)
        
        format_detail = QLabel("CSV, Excel (.xlsx, .xls)")
        format_detail.setFont(QFont("Segoe UI", 9))
        format_detail.setStyleSheet("color: #6b7280; margin-left: 15px;")
        info_container.addWidget(format_detail)
        
        info_container.addSpacing(4)
        
        size_label = QLabel("💾 Maximum File Size")
        size_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        size_label.setStyleSheet("color: #1f2937;")
        info_container.addWidget(size_label)
        
        size_detail = QLabel("50 MB")
        size_detail.setFont(QFont("Segoe UI", 9))
        size_detail.setStyleSheet("color: #6b7280; margin-left: 15px;")
        info_container.addWidget(size_detail)
        
        box_layout.addLayout(info_container)
        
        upload_container = QHBoxLayout()
        upload_container.addStretch()
        upload_container.addWidget(self.upload_box)
        upload_container.addStretch()
        layout.addLayout(upload_container)
        
        layout.addSpacing(20)
        
        self.progress_widget = ClickableFrame()
        self.progress_widget.setVisible(False)
        self.progress_widget.setFixedSize(350, 350)
        self.progress_widget.setStyleSheet("""
            ClickableFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border: 3px solid rgba(31, 41, 55, 0.2);
                border-radius: 28px;
            }
        """)
        
        progress_shadow = QGraphicsDropShadowEffect()
        progress_shadow.setBlurRadius(30)
        progress_shadow.setXOffset(0)
        progress_shadow.setYOffset(6)
        progress_shadow.setColor(QColor(0, 0, 0, 25))
        self.progress_widget.setGraphicsEffect(progress_shadow)
        
        progress_layout = QVBoxLayout(self.progress_widget)
        progress_layout.setAlignment(Qt.AlignCenter)
        progress_layout.setSpacing(15)
        progress_layout.setContentsMargins(25, 25, 25, 25)
        
        self.progress_label = QLabel("Analyzing your data...")
        self.progress_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("color: #111827;")
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 12px;
                text-align: center;
                height: 40px;
                font-size: 12px;
                font-weight: bold;
                background-color: rgba(229, 231, 235, 0.8);
                color: #1f2937;
            }
            QProgressBar::chunk {
                background-color: #1f2937;
                border-radius: 12px;
            }
        """)
        self.progress_bar.setMaximum(100)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #4b5563;")
        self.status_label.setWordWrap(True)
        progress_layout.addWidget(self.status_label)
        
        progress_container = QHBoxLayout()
        progress_container.addStretch()
        progress_container.addWidget(self.progress_widget)
        progress_container.addStretch()
        layout.addLayout(progress_container)
        
        layout.addSpacing(25)
        
        self.analyze_btn = QPushButton("Start Analysis")
        self.analyze_btn.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.analyze_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_btn.setMinimumWidth(320)
        self.analyze_btn.setFixedHeight(85)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                padding: 18px 50px;
                background-color: #1f2937;
                color: white;
                border: none;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:disabled {
                background-color: #d1d5db;
                color: #9ca3af;
            }
        """)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.clicked.connect(self.upload_file)
        
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(self.analyze_btn)
        button_container.addStretch()
        layout.addLayout(button_container)
        
        layout.addStretch()
    
    def resizeEvent(self, event):
        if not hasattr(self, 'navbar_widget'):
            if event:
                super().resizeEvent(event)
            return
        
        w = self.width()
        h = self.height()
        
        navbar_height = 120
        self.navbar_widget.setGeometry(0, 0, w, navbar_height)
        
        content_y = navbar_height
        content_height = h - navbar_height
        self.upload_content_widget.setGeometry(0, content_y, w, content_height)
        
        scale_x = w / self.BASE_WIDTH
        scale_y = h / self.BASE_HEIGHT
        
        for i, label in enumerate(self.diagram_labels):
            data = self.diagram_data[i]
            orig_pos = data["pos"]
            
            new_x = int(orig_pos[0] * scale_x)
            new_y = int(orig_pos[1] * scale_y)
            
            label.move(new_x, new_y)
        
        self.navbar_widget.raise_()
        self.upload_content_widget.raise_()
        
        if event:
            super().resizeEvent(event)
    
    def load_user_profile(self):
        response = api_client.get_profile()
        
        if "error" not in response:
            self.current_user = response
            username = response.get("username", "User")
            full_name = response.get("full_name", username)
            display_name = full_name.split()[0] if full_name else username
            self.profile_btn.setText(f"👤 {display_name} ")
        else:
            self.profile_btn.setText("👤 User ")
    
    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", 
            "Data Files (*.csv *.xlsx *.xls);;All Files (*)"
        )
        if file_path:
            self.selected_file = file_path
            import os
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            
            self.file_label.setText(f"✅ {file_name}\n📊 Size: {file_size:.2f} MB")
            self.file_label.setStyleSheet("color: #059669; font-weight: bold; font-size: 12px;")
            self.analyze_btn.setEnabled(True)
        else:
            if not self.selected_file:
                self.file_label.setText("Click anywhere to select file")
                self.file_label.setStyleSheet("color: #6b7280; font-size: 13px;")
                self.analyze_btn.setEnabled(False)
    
    def upload_file(self):
        if not self.selected_file:
            error_dialog = ErrorDialog("Error", "Please select a file first.", self)
            error_dialog.exec_()
            return
        
        self.progress_widget.setVisible(True)
        self.progress_bar.setValue(0)
        self.analyze_btn.setEnabled(False)
        self.upload_box.setVisible(False)
        
        self.upload_thread = UploadThread(self.selected_file)
        self.upload_thread.progress.connect(self.update_progress)
        self.upload_thread.status_message.connect(self.update_status)
        self.upload_thread.finished.connect(self.upload_complete)
        self.upload_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, message):
        self.status_label.setText(message)
    
    def upload_complete(self, result):
        self.analyze_btn.setEnabled(True)
        self.upload_box.setVisible(True)
        self.progress_widget.setVisible(False)
        
        if "error" in result:
            error_dialog = ErrorDialog("Upload Failed", result["error"], self)
            error_dialog.exec_()
        elif "upload_id" in result:
            self.show_results(result)
        else:
            error_dialog = ErrorDialog("Error", "Invalid response from server", self)
            error_dialog.exec_()
    
    def show_upload(self):
        pass
    
    def show_results(self, data):
        upload_id = data.get('upload_id')
        if not upload_id:
            error_dialog = ErrorDialog("Error", "No upload ID received from server", self)
            error_dialog.exec_()
            return
        self.results_window = ResultsWindow(upload_id)
        self.results_window.show()
        self.close()
    
    def show_dashboard(self):
        self.dashboard_window = DashboardWindow()
        self.dashboard_window.show()
        self.close()
    
    def show_history(self):
        self.history_window = HistoryWindow()
        self.history_window.show()
        self.close()
    
    def show_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()
    
    def show_profile(self):
        self.profile_window = ProfileWindow()
        self.profile_window.show()
        self.close()
    
    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            api_client.set_token(None)
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()