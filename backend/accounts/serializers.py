from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Upload  

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(max_length=255, required=False)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.CharField(max_length=20, required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['username', 'email', 'full_name', 'date_of_birth', 'gender', 'created_at']
        read_only_fields = ['created_at']

class UploadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    upload_date_formatted = serializers.SerializerMethodField()
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = Upload
        fields = [
            'id', 'upload_id', 'filename', 'username', 'rows', 'columns',
            'file_size', 'file_size_mb', 'column_names', 'data_types', 
            'missing_values', 'summary_stats', 'data_preview', 'status', # ADDED data_preview
            'upload_date', 'upload_date_formatted'
        ]
        read_only_fields = ['id', 'upload_id', 'upload_date', 'user']
    
    def get_upload_date_formatted(self, obj):
        """Format date as 'Nov 17, 2024'"""
        return obj.upload_date.strftime('%b %d, %Y')
    
    def get_file_size_mb(self, obj):
        """Convert bytes to MB"""
        return round(obj.file_size / (1024 * 1024), 2)