from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon


class LargeConfirmDialog(QDialog):
    """Beautiful large confirmation dialog"""
    
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(600, 350)  
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 600) // 2
            y = parent_geo.y() + (parent_geo.height() - 350) // 2
            self.move(x, y)
        
        self.setup_ui(title, message)
        self.result_value = False
    
    def setup_ui(self, title, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("⚠️")
        icon_label.setFont(QFont("Segoe UI Emoji", 48))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)
        
        header_layout.addSpacing(20)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title_label.setStyleSheet("color: #1f2937; background: transparent;")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)
        
        layout.addLayout(header_layout)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 16))
        message_label.setStyleSheet("color: #4b5563; background: transparent; line-height: 1.6;")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(message_label)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFixedHeight(60)
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 40px;
                background-color: #6b7280;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("Yes, Delete")
        confirm_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        confirm_btn.setCursor(Qt.PointingHandCursor)
        confirm_btn.setFixedHeight(60)
        confirm_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 40px;
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        confirm_btn.clicked.connect(self.accept)
        button_layout.addWidget(confirm_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 20px;
                border: 3px solid #e5e7eb;
            }
        """)


class LargeSuccessDialog(QDialog):
    """Beautiful large success dialog"""
    
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(550, 300)
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 550) // 2
            y = parent_geo.y() + (parent_geo.height() - 300) // 2
            self.move(x, y)
        
        self.setup_ui(title, message)
    
    def setup_ui(self, title, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("✅")
        icon_label.setFont(QFont("Segoe UI Emoji", 48))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)
        
        header_layout.addSpacing(20)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title_label.setStyleSheet("color: #059669; background: transparent;")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)
        
        layout.addLayout(header_layout)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 15))
        message_label.setStyleSheet("color: #4b5563; background: transparent;")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(message_label)
        
        layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setFixedHeight(60)
        ok_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 60px;
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 20px;
                border: 3px solid #d1fae5;
            }
        """)


class LargeErrorDialog(QDialog):
    """Beautiful large error dialog"""
    
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(550, 300)
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 550) // 2
            y = parent_geo.y() + (parent_geo.height() - 300) // 2
            self.move(x, y)
        
        self.setup_ui(title, message)
    
    def setup_ui(self, title, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("❌")
        icon_label.setFont(QFont("Segoe UI Emoji", 48))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)
        
        header_layout.addSpacing(20)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title_label.setStyleSheet("color: #dc2626; background: transparent;")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)
        
        layout.addLayout(header_layout)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 15))
        message_label.setStyleSheet("color: #4b5563; background: transparent;")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(message_label)
        
        layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setFixedHeight(60)
        ok_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 60px;
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 20px;
                border: 3px solid #fecaca;
            }
        """)


class LargeInfoDialog(QDialog):
    """Beautiful large info dialog"""
    
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(550, 300)
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 550) // 2
            y = parent_geo.y() + (parent_geo.height() - 300) // 2
            self.move(x, y)
        
        self.setup_ui(title, message)
    
    def setup_ui(self, title, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("ℹ️")
        icon_label.setFont(QFont("Segoe UI Emoji", 48))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)
        
        header_layout.addSpacing(20)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title_label.setStyleSheet("color: #2563eb; background: transparent;")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)
        
        layout.addLayout(header_layout)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 15))
        message_label.setStyleSheet("color: #4b5563; background: transparent;")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(message_label)
        
        layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setFixedHeight(60)
        ok_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 60px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 20px;
                border: 3px solid #dbeafe;
            }
        """)


class CompactConfirmDialog(QDialog):
    """Compact confirmation dialog for desktop"""
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(520, 380)  
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 520) // 2
            y = parent_geo.y() + (parent_geo.height() - 380) // 2
            self.move(x, y)
        
        self.setup_ui(title, message)
        self.result_value = False
    
    def setup_ui(self, title, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #1f2937; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 13)) 
        message_label.setStyleSheet("color: #4b5563; background: transparent; line-height: 1.5;")
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(460)
        layout.addWidget(message_label)
        
        layout.addSpacing(15)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFixedSize(140, 50)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                color: #1f2937;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #d1d5db;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("Confirm")
        confirm_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        confirm_btn.setCursor(Qt.PointingHandCursor)
        confirm_btn.setFixedSize(140, 50)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        confirm_btn.clicked.connect(self.accept)
        button_layout.addWidget(confirm_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
                border: 2px solid #e5e7eb;
            }
        """)


class CompactSuccessDialog(QDialog):
    """Compact success dialog"""
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(450, 280)
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 450) // 2
            y = parent_geo.y() + (parent_geo.height() - 280) // 2
            self.move(x, y)
        
        self.setup_ui(title, message)
    
    def setup_ui(self, title, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)
        
        icon_label = QLabel("✓")
        icon_label.setFont(QFont("Segoe UI", 50))
        icon_label.setStyleSheet("color: #059669; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #1f2937; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 13))
        message_label.setStyleSheet("color: #4b5563; background: transparent;")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        ok_btn = QPushButton("OK")
        ok_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setFixedSize(120, 45)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(ok_btn)
        btn_container.addStretch()
        layout.addLayout(btn_container)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
                border: 2px solid #d1fae5;
            }
        """)


class CompactErrorDialog(QDialog):
    """Compact error dialog"""
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(450, 280)
        
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 450) // 2
            y = parent_geo.y() + (parent_geo.height() - 280) // 2
            self.move(x, y)
        
        self.setup_ui(title, message)
    
    def setup_ui(self, title, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)
        
        icon_label = QLabel("✗")
        icon_label.setFont(QFont("Segoe UI", 50))
        icon_label.setStyleSheet("color: #dc2626; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #1f2937; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 13))
        message_label.setStyleSheet("color: #4b5563; background: transparent;")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        ok_btn = QPushButton("OK")
        ok_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setFixedSize(120, 45)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(ok_btn)
        btn_container.addStretch()
        layout.addLayout(btn_container)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
                border: 2px solid #fecaca;
            }
        """)