import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.error_dialog import ErrorDialog


class OTPDialog(QDialog):
    def __init__(self, email, api_client, parent=None):
        super().__init__(parent)
        self.email = email
        self.api_client = api_client
        self.otp_code = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Email Verification")
        self.setFixedSize(600, 650)
        self.setModal(True)
        
        if self.parent():
            parent_geo = self.parent().geometry()
            x = parent_geo.x() + (parent_geo.width() - 600) // 2
            y = parent_geo.y() + (parent_geo.height() - 650) // 2
            self.move(x, y)
        else:
            from PyQt5.QtWidgets import QDesktopWidget
            screen = QDesktopWidget().screenGeometry()
            x = (screen.width() - 600) // 2
            y = (screen.height() - 650) // 2
            self.move(x, y)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)
        
        layout.addSpacing(20)
        
        title = QLabel("Verify Your Email")
        title.setFont(QFont("Comic Sans MS", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #000000;")
        title.setWordWrap(True)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        email_info = QLabel("We've sent a 6-digit code to:")
        email_info.setFont(QFont("Inter", 12))
        email_info.setAlignment(Qt.AlignCenter)
        email_info.setWordWrap(True)
        email_info.setStyleSheet("color: #666666;")
        layout.addWidget(email_info)
        
        email_address = QLabel(self.email)
        email_address.setFont(QFont("Inter", 13, QFont.Bold))
        email_address.setAlignment(Qt.AlignCenter)
        email_address.setWordWrap(True)
        email_address.setStyleSheet("color: #000000; margin-top: 3px;")
        layout.addWidget(email_address)
        
        layout.addSpacing(20)
        
        otp_label = QLabel("Enter 6-Digit Code")
        otp_label.setFont(QFont("Inter", 10))
        otp_label.setStyleSheet("color: #000000;")
        layout.addWidget(otp_label)
        
        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("000000")
        self.otp_input.setMaxLength(6)
        self.otp_input.setAlignment(Qt.AlignCenter)
        self.otp_input.setFont(QFont("Inter", 20, QFont.Bold))
        self.otp_input.setFixedHeight(60)
        
        self.otp_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
                color: #000000;
                letter-spacing: 6px; 
            }
            QLineEdit:focus {
                border-color: #00BFFF;
            }
        """)
        layout.addWidget(self.otp_input)
        
        layout.addSpacing(20)
        
        self.verify_btn = QPushButton("Verify Account")
        self.verify_btn.setFont(QFont("Inter", 11, QFont.Bold))
        self.verify_btn.setCursor(Qt.PointingHandCursor)
        self.verify_btn.setFixedHeight(55)
        self.verify_btn.setStyleSheet("""
            QPushButton {
                padding: 16px 20px;
                background-color: #111111;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:disabled {
                background-color: #94a3b8;
            }
        """)
        self.verify_btn.clicked.connect(self.verify_otp)
        layout.addWidget(self.verify_btn)
        
        layout.addSpacing(15)
        
        resend_layout = QHBoxLayout()
        resend_layout.addStretch()
        
        resend_label = QLabel("Didn't receive the code?")
        resend_label.setFont(QFont("Inter", 10))
        resend_label.setStyleSheet("color: #333333;")
        resend_layout.addWidget(resend_label)
        
        self.resend_btn = QPushButton("Resend")
        self.resend_btn.setFont(QFont("Inter", 10, QFont.Bold))
        self.resend_btn.setCursor(Qt.PointingHandCursor)
        self.resend_btn.setStyleSheet("""
            QPushButton {
                color: #00BFFF;
                border: none;
                background: transparent;
                padding: 0px;
                margin-left: 5px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
            QPushButton:disabled {
                color: #94a3b8;
                text-decoration: none;
            }
        """)
        self.resend_btn.clicked.connect(self.resend_otp)
        resend_layout.addWidget(self.resend_btn)
        
        resend_layout.addStretch()
        layout.addLayout(resend_layout)
        
        layout.addSpacing(10)
        
        expiry_note = QLabel("The code will expire in 10 minutes")
        expiry_note.setFont(QFont("Inter", 9))
        expiry_note.setAlignment(Qt.AlignCenter)
        expiry_note.setStyleSheet("color: #64748b;")
        layout.addWidget(expiry_note)
        
        layout.addStretch() 
        self.setLayout(layout)
        
        self.setStyleSheet("background-color: #ffffff;")
    
    def verify_otp(self):
        otp = self.otp_input.text().strip()
        
        if len(otp) != 6:
            error_dialog = ErrorDialog("Invalid OTP", "Please enter a 6-digit code.", self)
            error_dialog.exec_()
            return
        
        self.verify_btn.setEnabled(False)
        self.verify_btn.setText("Verifying...")
        
        print(f"UI: Verifying OTP {otp} for {self.email}")
        response = self.api_client.verify_otp(self.email, otp)
        
        if "error" in response:
            error_dialog = ErrorDialog("Verification Failed", response["error"], self)
            error_dialog.exec_()
            self.verify_btn.setEnabled(True)
            self.verify_btn.setText("Verify Account")
        else:
            self.otp_code = otp
            QMessageBox.information(self, "Success", "Email verified successfully!")
            self.accept()
    
    def resend_otp(self):
        self.resend_btn.setEnabled(False)
        self.resend_btn.setText("Sending...")
        
        print(f"UI: Resending OTP for {self.email}")
        response = self.api_client.resend_otp(self.email)
        
        if "error" in response:
            error_dialog = ErrorDialog("Error", response["error"], self)
            error_dialog.exec_()
        else:
            QMessageBox.information(self, "OTP Sent", "A new code has been sent to your email")
        
        self.resend_btn.setEnabled(True)
        self.resend_btn.setText("Resend")