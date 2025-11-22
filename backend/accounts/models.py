from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
import string
class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def generate_otp(self):
        """Generate 6-digit OTP"""
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.expires_at = timezone.now() + timedelta(minutes=10)
        self.save()
        return self.otp
    
    def is_valid(self):
        """Check if OTP is still valid"""
        if not self.expires_at:
            return False
        return not self.verified and timezone.now() < self.expires_at
    
    def __str__(self):
        return f"{self.email} - {self.otp}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name or self.user.username

class Upload(models.Model):
    """Store file upload and analysis data"""
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    upload_id = models.CharField(max_length=100, unique=True)
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)

    rows = models.IntegerField(default=0)
    columns = models.IntegerField(default=0)
    file_size = models.BigIntegerField(default=0)

    column_names = models.JSONField(default=list)
    data_types = models.JSONField(default=dict)
    missing_values = models.JSONField(default=dict)
    summary_stats = models.JSONField(default=dict)
    data_preview = models.JSONField(default=list) 

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.filename} - {self.user.username}"