import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLineEdit, QComboBox, QHeaderView,
    QAbstractItemView, QFrame, QMenu, QAction,
    QGraphicsDropShadowEffect, QFileDialog, QDialog, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from api.django_client import api_client
from ui.error_dialog import ErrorDialog
import os


class DeleteThread(QThread):
    """Thread for deleting upload"""
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
    """Thread for downloading PDF"""
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


class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Upload History - Chemizer Analytics")
        self.setGeometry(50, 50, 1200, 800)
        
        self.showMaximized()
        
        self.setStyleSheet("background-color: #f3f4f6;")
        
        self.all_uploads = []
        self.filtered_uploads = []
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f3f4f6;")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.setup_navbar()
        main_layout.addWidget(self.navbar_widget)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f3f4f6; }")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #f3f4f6;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Upload History")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #1f2937; background: transparent;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                background-color: #1f2937;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
        """)
        refresh_btn.clicked.connect(self.load_history)
        header_layout.addWidget(refresh_btn)
        
        content_layout.addLayout(header_layout)
        
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        search_label = QLabel("🔍")
        search_label.setFont(QFont("Segoe UI Emoji", 16))
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by filename...")
        self.search_input.setFont(QFont("Segoe UI", 12))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1f2937;
            }
        """)
        self.search_input.textChanged.connect(self.filter_history)
        filter_layout.addWidget(self.search_input, 3)
        
        filter_label = QLabel("Status:")
        filter_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        filter_label.setStyleSheet("color: #1f2937; background: transparent;")
        filter_layout.addWidget(filter_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Completed", "Processing", "Failed"])
        self.status_filter.setFont(QFont("Segoe UI", 11))
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #1f2937;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #1f2937;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #1f2937;
                border-radius: 8px;
                background-color: white;
                selection-background-color: rgba(31, 41, 55, 0.1);
                padding: 5px;
                font-size: 11px;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px;
                min-height: 30px;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.filter_history)
        filter_layout.addWidget(self.status_filter, 1)
        
        sort_label = QLabel("Sort by:")
        sort_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        sort_label.setStyleSheet("color: #1f2937; background: transparent;")
        filter_layout.addWidget(sort_label)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Newest First", "Oldest First", "Filename A-Z", "Filename Z-A"])
        self.sort_combo.setFont(QFont("Segoe UI", 11))
        self.sort_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #1f2937;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #1f2937;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #1f2937;
                border-radius: 8px;
                background-color: white;
                selection-background-color: rgba(31, 41, 55, 0.1);
                padding: 5px;
                font-size: 11px;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px;
                min-height: 30px;
            }
        """)
        self.sort_combo.currentTextChanged.connect(self.sort_history)
        filter_layout.addWidget(self.sort_combo, 1)
        
        content_layout.addLayout(filter_layout)
        
        self.history_table = QTableWidget()
        self.history_table.setStyleSheet("""
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
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setAlternatingRowColors(True)
        
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_layout.addWidget(self.history_table)
        
        self.info_label = QLabel("")
        self.info_label.setFont(QFont("Segoe UI", 11))
        self.info_label.setStyleSheet("color: #6b7280; background: transparent;")
        content_layout.addWidget(self.info_label)
        
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
        central_widget.setLayout(main_layout)
        
        self.load_user_profile()
        
        self.load_history()
    
    def setup_navbar(self):
        """Create the top navigation bar"""
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
        
        self.history_nav_btn = self.create_nav_button("📜 History", True)
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
        """Create navigation button"""
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
        """Load user profile from API"""
        response = api_client.get_profile()
        
        if "error" not in response:
            username = response.get("username", "User")
            full_name = response.get("full_name", username)
            display_name = full_name.split()[0] if full_name else username
            self.profile_btn.setText(f"👤 {display_name} ")
        else:
            self.profile_btn.setText("👤 User ")
    
    def load_history(self):
        """Load upload history from API"""
        response = api_client.get_upload_history()
        
        if "error" in response:
            error_dialog = ErrorDialog("Error", f"Failed to load history: {response['error']}", self)
            error_dialog.exec_()
            self.all_uploads = []
        else:
            self.all_uploads = response.get("uploads", [])
        
        self.filtered_uploads = self.all_uploads.copy()
        self.populate_table()
    
    def populate_table(self):
        """Populate table with upload data"""
        uploads = self.filtered_uploads
        
        self.history_table.setRowCount(len(uploads))
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "ID", "Filename", "Upload Date", "Rows", "Status", "Actions"
        ])
        
        header = self.history_table.horizontalHeader()
        header.setFont(QFont("Segoe UI", 13, QFont.Bold))
        
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.resizeSection(0, 70)
        
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.resizeSection(2, 180)
        
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 90)
        
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.resizeSection(4, 140)
        
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.resizeSection(5, 100)
        
        for row_idx, upload in enumerate(uploads):
            self.history_table.setRowHeight(row_idx, 55)
            
            if row_idx % 2 == 0:
                row_color = QColor("#f9fafb")
            else:
                row_color = QColor("#ffffff")
            
            id_item = QTableWidgetItem(str(upload.get("id", "")))
            id_item.setFont(QFont("Segoe UI", 12, QFont.Bold))
            id_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            id_item.setBackground(row_color)
            id_item.setForeground(QColor("#1f2937"))
            self.history_table.setItem(row_idx, 0, id_item)
            
            filename = upload.get("filename", "N/A")
            filename_item = QTableWidgetItem(filename)
            filename_item.setFont(QFont("Segoe UI", 12, QFont.Bold))
            filename_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            filename_item.setBackground(row_color)
            filename_item.setForeground(QColor("#1f2937"))
            filename_item.setToolTip(filename)
            self.history_table.setItem(row_idx, 1, filename_item)
            
            date_item = QTableWidgetItem(upload.get("upload_date_formatted", "N/A"))
            date_item.setFont(QFont("Segoe UI", 11))
            date_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            date_item.setBackground(row_color)
            date_item.setForeground(QColor("#4b5563"))
            self.history_table.setItem(row_idx, 2, date_item)
            
            rows_item = QTableWidgetItem(str(upload.get("rows", "N/A")))
            rows_item.setFont(QFont("Segoe UI", 12, QFont.Bold))
            rows_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            rows_item.setBackground(row_color)
            rows_item.setForeground(QColor("#2563eb"))
            self.history_table.setItem(row_idx, 3, rows_item)
            
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
            self.history_table.setCellWidget(row_idx, 4, status_widget)
            
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
            self.history_table.setCellWidget(row_idx, 5, btn_container)
        
        total_height = self.history_table.horizontalHeader().height()
        for row in range(len(uploads)):
            total_height += self.history_table.rowHeight(row)
        
        self.history_table.setMinimumHeight(total_height + 10)
        self.history_table.setMaximumHeight(total_height + 10)
        
        total = len(self.all_uploads)
        showing = len(self.filtered_uploads)
        self.info_label.setText(f"Showing {showing} of {total} uploads")
    
    def filter_history(self):
        """Filter uploads based on search and status"""
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()
        
        self.filtered_uploads = []
        
        for upload in self.all_uploads:
            filename = upload.get("filename", "").lower()
            if search_text and search_text not in filename:
                continue
            
            status = upload.get("status", "")
            if status_filter != "All" and status != status_filter:
                continue
            
            self.filtered_uploads.append(upload)
        
        self.sort_history()
    
    def sort_history(self):
        """Sort filtered uploads"""
        sort_by = self.sort_combo.currentText()
        
        if sort_by == "Newest First":
            self.filtered_uploads.sort(key=lambda x: x.get("upload_date", ""), reverse=True)
        elif sort_by == "Oldest First":
            self.filtered_uploads.sort(key=lambda x: x.get("upload_date", ""))
        elif sort_by == "Filename A-Z":
            self.filtered_uploads.sort(key=lambda x: x.get("filename", "").lower())
        elif sort_by == "Filename Z-A":
            self.filtered_uploads.sort(key=lambda x: x.get("filename", "").lower(), reverse=True)
        
        self.populate_table()
    
    def view_upload(self, upload):
        """View upload details/results"""
        from ui.results_window import ResultsWindow
        self.results_window = ResultsWindow(upload)
        self.results_window.show()
        self.close()
    
    def download_pdf(self, upload):
        """Download PDF report"""
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
        """Handle download completion"""
        from ui.custom_dialogs import LargeSuccessDialog, LargeErrorDialog
        
        if success:
            dialog = LargeSuccessDialog("Download Complete!", message, self)
            dialog.exec_()
        else:
            dialog = LargeErrorDialog("Download Failed", message, self)
            dialog.exec_()
    
    def delete_upload(self, upload):
        """Delete an upload"""
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
        """Handle delete completion"""
        from ui.custom_dialogs import LargeSuccessDialog, LargeErrorDialog
        
        if success:
            dialog = LargeSuccessDialog("Success!", message, self)
            dialog.exec_()
            self.load_history()
        else:
            dialog = LargeErrorDialog("Delete Failed", message, self)
            dialog.exec_()
    
    def show_upload(self):
        """Navigate to upload page"""
        from ui.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
    
    def show_dashboard(self):
        """Navigate to dashboard"""
        from ui.dashboard_window import DashboardWindow
        self.dashboard_window = DashboardWindow()
        self.dashboard_window.show()
        self.close()
    
    def show_history(self):
        """Already on history page"""
        pass
    
    def show_settings(self):
        """Navigate to settings"""
        from ui.settings_window import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.close()
    
    def show_profile(self):
        """Navigate to profile"""
        from ui.profile_window import ProfileWindow
        self.profile_window = ProfileWindow()
        self.profile_window.show()
        self.close()
    
    def logout(self):
        """Logout user"""
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