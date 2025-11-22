import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView,
    QAbstractItemView, QFrame, QMenu, QAction,
    QGraphicsDropShadowEffect, QFileDialog, QDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from api.django_client import api_client
from ui.error_dialog import ErrorDialog
import os


class DeleteThread(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self, upload_id):
        super().__init__()
        self.upload_id = upload_id
    
    def run(self):
        try:
            result = api_client.delete_upload(self.upload_id)
            if "error" in result:
                self.finished.emit(False, result["error"])
            else:
                self.finished.emit(True, "Upload deleted successfully")
        except Exception as e:
            self.finished.emit(False, str(e))


class DownloadThread(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self, upload_id, save_path):
        super().__init__()
        self.upload_id = upload_id
        self.save_path = save_path
    
    def run(self):
        try:
            result = api_client.download_pdf_report(self.upload_id, self.save_path)
            if "error" in result:
                self.finished.emit(False, result["error"])
            else:
                self.finished.emit(True, f"PDF saved to: {self.save_path}")
        except Exception as e:
            self.finished.emit(False, str(e))


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard - Chemizer Analytics")
        self.setGeometry(50, 50, 1200, 800)
        
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
        
        self.setup_dashboard_content()
        layout.addWidget(self.scroll_area)
        
        central_widget.setLayout(layout)
        
        self.load_user_profile()
        
        self.load_dashboard_data()
    
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
        
        self.dashboard_nav_btn = self.create_nav_button("📊 Dashboard", True)
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
    
    def load_user_profile(self):
        response = api_client.get_profile()
        
        if "error" not in response:
            username = response.get("username", "User")
            full_name = response.get("full_name", username)
            display_name = full_name.split()[0] if full_name else username
            self.profile_btn.setText(f"👤 {display_name} ")
        else:
            self.profile_btn.setText("👤 User ")
    
    def setup_dashboard_content(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f3f4f6; }")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #f3f4f6;")
        self.scroll_area.setWidget(scroll_content)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(25)
        
        header_layout = QHBoxLayout()
        
        self.welcome_label = QLabel("Welcome back!")
        self.welcome_label.setFont(QFont("Comic Sans MS", 32, QFont.Bold))
        self.welcome_label.setStyleSheet("color: #000000; background: transparent;")
        header_layout.addWidget(self.welcome_label)
        
        header_layout.addStretch()
        
        upload_btn = QPushButton("📤 New Upload")
        upload_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.setStyleSheet("""
            QPushButton {
                padding: 16px 40px;
                background-color: #1f2937;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
        """)
        upload_btn.clicked.connect(self.show_upload)
        header_layout.addWidget(upload_btn)
        
        layout.addLayout(header_layout)
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.total_card = self.create_stat_card("📤 Total Uploads", "0", "#00BFFF")
        stats_layout.addWidget(self.total_card)
        
        self.analyses_card = self.create_stat_card("📊 Analyses", "0", "#059669")
        stats_layout.addWidget(self.analyses_card)
        
        self.success_card = self.create_stat_card("✓ Success Rate", "0%", "#8b5cf6")
        stats_layout.addWidget(self.success_card)
        
        layout.addLayout(stats_layout)
        
        activity_header = QHBoxLayout()
        
        activity_label = QLabel("Recent Activity")
        activity_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        activity_label.setStyleSheet("color: #1f2937; background: transparent;")
        activity_header.addWidget(activity_label)
        
        activity_header.addStretch()
        
        view_all_btn = QPushButton("View All →")
        view_all_btn.setFont(QFont("Segoe UI", 14))
        view_all_btn.setCursor(Qt.PointingHandCursor)
        view_all_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                background-color: transparent;
                color: #00BFFF;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        view_all_btn.clicked.connect(self.show_history)
        activity_header.addWidget(view_all_btn)
        
        layout.addLayout(activity_header)
        
        self.activity_table = QTableWidget()
        self.activity_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #2563eb;
                border-radius: 16px;
                background-color: white;
                gridline-color: #e5e7eb;
            }
            QHeaderView::section {
                background-color: #1f2937;
                padding: 14px 10px;
                border: none;
                font-weight: bold;
                font-size: 13px;
                color: white;
                text-align: center;
                border-right: 1px solid #374151;
            }
            QHeaderView::section:first {
                border-top-left-radius: 14px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 14px;
                border-right: none;
            }
            QTableWidget::item {
                padding: 10px 8px;
                border-bottom: 1px solid #e5e7eb;
                font-size: 12px;
                color: #1f2937;
            }
            QTableWidget::item:selected {
                background-color: #e0f2fe;
                color: #1f2937;
            }
            QTableWidget::item:hover {
                background-color: #f0f9ff;
            }
        """)
        self.activity_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.activity_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.activity_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.activity_table.verticalHeader().setVisible(False)
        self.activity_table.setAlternatingRowColors(True)
        
        self.activity_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.activity_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        layout.addWidget(self.activity_table)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
    
    def create_stat_card(self, label, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 12px;
                padding: 20px;
                border: 2px solid #e5e7eb;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 40, QFont.Bold))
        value_label.setStyleSheet(f"color: {color}; background: transparent;")
        card_layout.addWidget(value_label)
        
        title_label = QLabel(label)
        title_label.setFont(QFont("Segoe UI", 15))
        title_label.setStyleSheet("color: #666666; background: transparent;")
        card_layout.addWidget(title_label)
        
        card.value_label = value_label
        
        return card
    
    def load_dashboard_data(self):
        profile = api_client.get_profile()
        if "error" not in profile:
            full_name = profile.get("full_name", "User")
            first_name = full_name.split()[0] if full_name else "User"
            self.welcome_label.setText(f"Welcome back, {first_name}!")
        
        response = api_client.get_upload_history()
        
        if "error" in response:
            error_dialog = ErrorDialog("Error", f"Failed to load data: {response['error']}", self)
            error_dialog.exec_()
            history = []
        else:
            history = response.get("uploads", [])
        
        total_uploads = len(history)
        completed = len([u for u in history if u.get("status") == "Completed"])
        success_rate = (completed / total_uploads * 100) if total_uploads > 0 else 0
        
        self.total_card.value_label.setText(str(total_uploads))
        self.analyses_card.value_label.setText(str(completed))
        self.success_card.value_label.setText(f"{success_rate:.1f}%")
        
        self.populate_activity(history)
    
    def populate_activity(self, uploads):
        self.activity_table.setRowCount(len(uploads))
        self.activity_table.setColumnCount(5)
        self.activity_table.setHorizontalHeaderLabels([
            "Status", "Filename", "Date", "Rows", "Actions"
        ])
        
        header = self.activity_table.horizontalHeader()
        header.setFont(QFont("Segoe UI", 13, QFont.Bold))
        
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.resizeSection(0, 140)
        
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.resizeSection(2, 180)
        
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 90)
        
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.resizeSection(4, 100)
        
        for row_idx, upload in enumerate(uploads):
            self.activity_table.setRowHeight(row_idx, 55)
            
            if row_idx % 2 == 0:
                row_color = QColor("#f9fafb")
            else:
                row_color = QColor("#ffffff")
            
            status = upload.get("status", "Unknown")
            status_widget = QWidget()
            status_widget.setStyleSheet(f"background: {row_color.name()}; border: none;")
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(0, 0, 0, 0)
            status_layout.setSpacing(0)
            
            status_label = QLabel()
            if status == "Completed":
                status_label.setText("✓ DONE")
                status_label.setStyleSheet("color: #059669; font-weight: bold; font-size: 11px; background: transparent; padding: 8px;")
            elif status == "Processing":
                status_label.setText("⏳ PROCESS")
                status_label.setStyleSheet("color: #f59e0b; font-weight: bold; font-size: 11px; background: transparent; padding: 8px;")
            else:
                status_label.setText("✗ FAILED")
                status_label.setStyleSheet("color: #dc2626; font-weight: bold; font-size: 11px; background: transparent; padding: 8px;")
            
            status_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            status_label.setAlignment(Qt.AlignCenter)
            status_layout.addStretch()
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            self.activity_table.setCellWidget(row_idx, 0, status_widget)
            
            filename = upload.get("filename", "N/A")
            filename_item = QTableWidgetItem(filename)
            filename_item.setFont(QFont("Segoe UI", 12, QFont.Bold))
            filename_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            filename_item.setBackground(row_color)
            filename_item.setForeground(QColor("#1f2937"))
            filename_item.setToolTip(filename)
            self.activity_table.setItem(row_idx, 1, filename_item)
            
            date_item = QTableWidgetItem(upload.get("upload_date_formatted", "N/A"))
            date_item.setFont(QFont("Segoe UI", 11))
            date_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            date_item.setBackground(row_color)
            date_item.setForeground(QColor("#4b5563"))
            self.activity_table.setItem(row_idx, 2, date_item)
            
            rows_item = QTableWidgetItem(str(upload.get("rows", "N/A")))
            rows_item.setFont(QFont("Segoe UI", 12, QFont.Bold))
            rows_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            rows_item.setBackground(row_color)
            rows_item.setForeground(QColor("#2563eb"))
            self.activity_table.setItem(row_idx, 3, rows_item)
            
            actions_btn = QPushButton("⋮")
            actions_btn.setFont(QFont("Segoe UI", 22, QFont.Bold))
            actions_btn.setCursor(Qt.PointingHandCursor)
            actions_btn.setFixedSize(32, 32)
            actions_btn.setStyleSheet(f"""
                QPushButton {{
                    padding: 0px;
                    background-color: white;
                    color: #1f2937;
                    border: 2px solid #2563eb;
                    border-radius: 10px;
                }}
                QPushButton:hover {{
                    background-color: #f0f9ff;
                    border-color: #1d4ed8;
                }}
                QPushButton:pressed {{
                    background-color: #e0f2fe;
                }}
            """)
            
            btn_container = QWidget()
            btn_container.setStyleSheet(f"background: {row_color.name()}; border: none;")
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(0)
            btn_layout.addStretch()
            btn_layout.addWidget(actions_btn, alignment=Qt.AlignCenter)
            btn_layout.addStretch()
            
            actions_menu = QMenu(self)
            actions_menu.setStyleSheet("""
                QMenu {
                    background-color: #ffffff;
                    border: 3px solid #2563eb;
                    border-radius: 12px;
                    padding: 10px;
                    min-width: 240px;
                }
                QMenu::item {
                    color: #1f2937;
                    padding: 14px 24px;
                    border-radius: 8px;
                    margin: 3px 0px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QMenu::item:selected {
                    background-color: #2563eb;
                    color: white;
                }
                QMenu::separator {
                    height: 2px;
                    background-color: #e5e7eb;
                    margin: 6px 10px;
                }
            """)
            
            view_action = QAction("👁️  View Analysis", self)
            view_action.setFont(QFont("Segoe UI", 14, QFont.Bold))
            view_action.triggered.connect(lambda checked, u=upload: self.view_upload(u))
            actions_menu.addAction(view_action)
            
            download_action = QAction("📥  Download PDF", self)
            download_action.setFont(QFont("Segoe UI", 14, QFont.Bold))
            download_action.triggered.connect(lambda checked, u=upload: self.download_pdf(u))
            actions_menu.addAction(download_action)
            
            actions_menu.addSeparator()
            
            delete_action = QAction("🗑️  Delete Upload", self)
            delete_action.setFont(QFont("Segoe UI", 14, QFont.Bold))
            delete_action.triggered.connect(lambda checked, u=upload: self.delete_upload(u))
            actions_menu.addAction(delete_action)
            
            actions_btn.setMenu(actions_menu)
            self.activity_table.setCellWidget(row_idx, 4, btn_container)
        
        total_height = self.activity_table.horizontalHeader().height()
        for row in range(len(uploads)):
            total_height += self.activity_table.rowHeight(row)
        
        self.activity_table.setMinimumHeight(total_height + 10)
        self.activity_table.setMaximumHeight(total_height + 10)
    
    def view_upload(self, upload):
        upload_id = upload.get("upload_id")
        
        from ui.results_window import ResultsWindow
        self.results_window = ResultsWindow(upload)
        self.results_window.show()
        self.close()
    
    def download_pdf(self, upload):
        upload_id = upload.get("upload_id")
        filename = upload.get("filename", "report")
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"analysis_report_{filename}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if save_path:
            self.download_thread = DownloadThread(upload_id, save_path)
            self.download_thread.finished.connect(self.download_complete)
            self.download_thread.start()
    
    def download_complete(self, success, message):
        from ui.custom_dialogs import LargeSuccessDialog, LargeErrorDialog
        
        if success:
            dialog = LargeSuccessDialog("Download Complete!", message, self)
            dialog.exec_()
        else:
            dialog = LargeErrorDialog("Download Failed", message, self)
            dialog.exec_()
    
    def delete_upload(self, upload):
        from ui.custom_dialogs import LargeConfirmDialog
        
        filename = upload.get("filename", "this upload")
        upload_id = upload.get("upload_id")
        
        dialog = LargeConfirmDialog(
            "Delete Upload?",
            f"Are you sure you want to delete '{filename}'?\n\n"
            "This action cannot be undone and will permanently remove:\n"
            "• The uploaded file\n"
            "• All analysis data\n"
            "• Generated reports",
            self
        )
        
        if dialog.exec_() == QDialog.Accepted:
            self.delete_thread = DeleteThread(upload_id)
            self.delete_thread.finished.connect(self.delete_complete)
            self.delete_thread.start()
    
    def delete_complete(self, success, message):
        from ui.custom_dialogs import LargeSuccessDialog, LargeErrorDialog
        
        if success:
            dialog = LargeSuccessDialog("Success!", message, self)
            dialog.exec_()
            self.load_dashboard_data()
        else:
            dialog = LargeErrorDialog("Delete Failed", message, self)
            dialog.exec_()
    
    def show_upload(self):
        from ui.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
    
    def show_dashboard(self):
        pass
    
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
    
    def show_profile(self):
        from ui.profile_window import ProfileWindow
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