import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel,
                             QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ErrorDialog(QDialog):
    """
    A custom, styled dialog box for showing errors, warnings, or info.
    It matches the look and feel of the OTPDialog.
    """
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setup_ui(title, message)
    
    def setup_ui(self, title_text, message_text):
        self.setFixedSize(450, 350) 
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)
        
        icon_label = QLabel("⚠️")
        icon_label.setFont(QFont("Inter", 60))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(icon_label)
        
        title = QLabel(title_text)
        title.setFont(QFont("Comic Sans MS", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #000000;")
        layout.addWidget(title)
        
        message_label = QLabel(message_text)
        message_label.setFont(QFont("Inter", 12))
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("color: #666666; margin-top: 5px;")
        layout.addWidget(message_label)
        
        layout.addStretch()
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFont(QFont("Inter", 12, QFont.Bold))
        self.ok_btn.setCursor(Qt.PointingHandCursor)
        self.ok_btn.setStyleSheet("""
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
        self.ok_btn.clicked.connect(self.accept) 
        
        self.setLayout(layout)
        
        self.setStyleSheet("background-color: #ffffff;")