from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import EmailOTP, Profile, Upload
from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    ResendOTPSerializer,
    ProfileSerializer,
    UploadSerializer
)
from google.auth.transport import requests
from google.oauth2 import id_token
import os
import traceback
import pandas as pd
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.http import FileResponse, HttpResponse
import io
from datetime import datetime
import glob
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except:
    HAS_MATPLOTLIB = False


def send_otp_email(email, otp):
    """Send OTP via email"""
    try:
        subject = 'Verify Your Email - Chemizer Analytics'
        message = f'''Your OTP verification code is: {otp}

This code will expire in 10 minutes.

If you did not request this, please ignore this email.

Best regards,
Chemizer Analytics Team'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print(f"OTP email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upload_history(request):
    """Get all uploads for the authenticated user"""
    print("=" * 50)
    print(f"📜 UPLOAD HISTORY - User: {request.user.username}")
    print("=" * 50)
    
    try:
        uploads = Upload.objects.filter(user=request.user).order_by('-upload_date')
        
        upload_list = []
        for upload in uploads:
            upload_list.append({
                'id': upload.id,
                'upload_id': str(upload.upload_id),
                'filename': upload.filename,
                'upload_date': upload.upload_date.isoformat(),
                'upload_date_formatted': upload.upload_date.strftime('%b %d, %Y'),
                'rows': upload.rows or 0,
                'file_size': upload.file_size or 0,
                'status': upload.status,
            })
        
        print(f"✅ Found {len(upload_list)} uploads for {request.user.username}")
        
        return Response({
            'uploads': upload_list
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Error fetching upload history: {str(e)}")
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    try:
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return Response(
                {"error": "Both current and new password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        if not user.check_password(current_password):
            return Response(
                {"error": "Current password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 8:
            return Response(
                {"error": "New password must be at least 8 characters"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register new user and send OTP"""
    print("=" * 50)
    print(f"Registration attempt - Received data: {request.data}")
    print(f"Content-Type: {request.content_type}")
    print(f"Request method: {request.method}")
    print("=" * 50)
    
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
            print(f"Validated data: {serializer.validated_data}")
            
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                is_active=False
            )
            print(f"User created: {user.username}")
            
            Profile.objects.create(
                user=user,
                full_name=serializer.validated_data.get('full_name', ''),
                date_of_birth=serializer.validated_data.get('date_of_birth'),
                gender=serializer.validated_data.get('gender')
            )
            print(f"Profile created for user: {user.username}")
            
            otp_obj = EmailOTP.objects.create(
                email=user.email,
                user=user
            )
            otp_code = otp_obj.generate_otp()
            print(f"OTP generated: {otp_code}")
            
            if send_otp_email(user.email, otp_code):
                return Response({
                    'message': 'Registration successful! OTP sent to your email.',
                    'email': user.email,
                    'requires_otp': True
                }, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response({
                    'error': 'Failed to send OTP email. Please check your email settings.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Registration error: {str(e)}")
            traceback.print_exc()
            return Response({
                'error': f'Registration failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    print(f"Validation failed - Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login and send OTP"""
    print("=" * 50)
    print(f"Login attempt - Received data: {request.data}")
    print("=" * 50)
    
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user is None:
            print(f"Authentication failed for username: {serializer.validated_data['username']}")
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        print(f"User authenticated: {user.username}")
        
        EmailOTP.objects.filter(user=user, verified=False).delete()
        
        otp_obj = EmailOTP.objects.create(
            email=user.email,
            user=user
        )
        otp_code = otp_obj.generate_otp()
        print(f"Login OTP generated: {otp_code}")
        
        if send_otp_email(user.email, otp_code):
            return Response({
                'message': 'OTP sent to your email.',
                'email': user.email,
                'requires_otp': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to send OTP email. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    print(f"Login validation failed - Errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """Verify OTP and log user in"""
    print("=" * 50)
    print(f"OTP verification - Received data: {request.data}")
    print("=" * 50)
    
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp']
        
        try:
            otp_obj = EmailOTP.objects.filter(
                email=email,
                otp=otp_code,
                verified=False
            ).latest('created_at')
            
            if not otp_obj.is_valid():
                print(f"OTP expired for email: {email}")
                return Response({
                    'error': 'OTP has expired. Please request a new one.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            otp_obj.verified = True
            otp_obj.save()
            print(f"OTP verified for email: {email}")
            
            user = otp_obj.user
            if not user.is_active:
                user.is_active = True
                user.save()
                print(f"User activated: {user.username}")
            
            token, _ = Token.objects.get_or_create(user=user)
            
            profile = Profile.objects.get(user=user)
            
            print(f"Login successful for user: {user.username}")
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': profile.full_name,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
            
        except EmailOTP.DoesNotExist:
            print(f"Invalid OTP for email: {email}")
            return Response({
                'error': 'Invalid OTP code'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    print(f"OTP verification validation failed - Errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    """Resend OTP to user email"""
    print("=" * 50)
    print(f"Resend OTP - Received data: {request.data}")
    print("=" * 50)
    
    serializer = ResendOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            EmailOTP.objects.filter(user=user, verified=False).delete()
            
            otp_obj = EmailOTP.objects.create(
                email=email,
                user=user
            )
            otp_code = otp_obj.generate_otp()
            print(f"New OTP generated for {email}: {otp_code}")
            
            if send_otp_email(email, otp_code):
                return Response({
                    'message': 'New OTP sent to your email.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to send OTP email.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except User.DoesNotExist:
            print(f"Email not found: {email}")
            return Response({
                'error': 'Email not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    print(f"Resend OTP validation failed - Errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Get user profile"""
    try:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update user profile"""
    print("=" * 50)
    print(f"Update profile - User: {request.user.username}, Data: {request.data}")
    print("=" * 50)
    
    try:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            print(f"Profile updated for user: {request.user.username}")
            return Response({
                'message': 'Profile updated successfully',
                'data': serializer.data
            })
        
        print(f"Profile update validation failed - Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Delete user account"""
    username = request.user.username
    request.user.delete()
    print(f"Account deleted: {username}")
    return Response({
        'message': 'Account deleted successfully'
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """Handle Google OAuth login"""
    print("=" * 50)
    print(f"Google login attempt - Received data: {request.data}")
    print("=" * 50)
    
    try:
        token = request.data.get('token')
        
        if not token:
            return Response({
                'error': 'No token provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
        
        if not client_id:
            print("Google OAuth not configured - missing GOOGLE_OAUTH_CLIENT_ID")
            return Response({
                'error': 'Google OAuth not configured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                client_id
            )
            
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            full_name = idinfo.get('name', f'{first_name} {last_name}')
            
            if not email:
                return Response({
                    'error': 'Email not provided by Google'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"Google token verified for email: {email}")
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0] + str(User.objects.filter(username__startswith=email.split('@')[0]).count()),
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True
                }
            )
            
            if created:
                print(f"New user created via Google: {user.username}")
            else:
                print(f"Existing user logged in via Google: {user.username}")
            
            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': full_name
                }
            )
            
            auth_token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': auth_token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': profile.full_name,
                'is_new_user': created,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            print(f"Invalid Google token: {str(e)}")
            traceback.print_exc()
            return Response({
                'error': f'Invalid Google token: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        print(f"Google authentication error: {str(e)}")
        traceback.print_exc()
        return Response({
            'error': f'Google authentication failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """Handle file upload and analysis"""
    print("=" * 50)
    print(f"📤 FILE UPLOAD - User: {request.user.username}")
    print(f"Files: {request.FILES}")
    print("=" * 50)
    
    if 'file' not in request.FILES:
        return Response({
            'error': 'No file provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    uploaded_file = request.FILES['file']
    file_name = uploaded_file.name
    
    allowed_extensions = ['.csv', '.xlsx', '.xls']
    file_ext = os.path.splitext(file_name)[1].lower()
    
    if file_ext not in allowed_extensions:
        return Response({
            'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        upload_id = str(uuid.uuid4())
        print(f"📊 Generated Upload ID: {upload_id}")
        
        file_path = default_storage.save(
            f'uploads/{request.user.username}/{upload_id}_{file_name}',
            ContentFile(uploaded_file.read())
        )
        
        full_path = default_storage.path(file_path)
        file_size = os.path.getsize(full_path)
        
        print(f"💾 File saved: {file_path} ({file_size} bytes)")
        
        if file_ext == '.csv':
            df = pd.read_csv(full_path)
        else:
            df = pd.read_excel(full_path)
        
        print(f"📈 File analyzed: {df.shape[0]} rows, {df.shape[1]} columns")
        
        preview_df = df.head(100).fillna('N/A')
        data_preview = preview_df.to_dict(orient='records')
        
        numeric_df = df.select_dtypes(include=['number'])
        summary_stats = numeric_df.describe().to_dict() if not numeric_df.empty else {}
        
        upload_obj = Upload.objects.create(
            user=request.user,
            upload_id=upload_id,
            filename=file_name,
            file_path=file_path,
            rows=df.shape[0],
            columns=df.shape[1],
            file_size=file_size,
            column_names=list(df.columns),
            data_types={col: str(dtype) for col, dtype in df.dtypes.items()},
            missing_values=df.isnull().sum().to_dict(),
            summary_stats=summary_stats,
            data_preview=data_preview,
            status='Completed'
        )
        
        print(f"✅ Upload saved to database - ID: {upload_obj.id}")
        
        analysis = {
            'upload_id': upload_id,
            'file_name': file_name,
            'rows': df.shape[0],
            'columns': df.shape[1],
            'column_names': list(df.columns),
            'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'missing_values': df.isnull().sum().to_dict(),
            'summary_stats': summary_stats,
            'data_preview': data_preview,
            'message': 'File uploaded and analyzed successfully'
        }
        
        print(f"🎉 Analysis complete for upload_id: {upload_id}")
        
        return Response(analysis, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ File upload error: {str(e)}")
        traceback.print_exc()
        return Response({
            'error': f'File processing failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_upload_history(request):
    """Get user's upload history"""
    print("=" * 50)
    print(f"📜 FETCH HISTORY - User: {request.user.username}")
    print("=" * 50)
    
    try:
        uploads = Upload.objects.filter(user=request.user).order_by('-upload_date')
        serializer = UploadSerializer(uploads, many=True)
        
        print(f"✅ Found {len(serializer.data)} uploads for {request.user.username}")
        
        return Response({
            'uploads': serializer.data,
            'total': len(serializer.data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Error fetching history: {str(e)}")
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_upload_detail(request, upload_id):
    """Get detailed information about a specific upload"""
    print("=" * 50)
    print(f"🔍 FETCH UPLOAD DETAIL - User: {request.user.username}, Upload ID: {upload_id}")
    print("=" * 50)
    
    try:
        upload = Upload.objects.get(upload_id=upload_id, user=request.user)
        serializer = UploadSerializer(upload)
        
        print(f"✅ Upload detail found: {upload.filename}")
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Upload.DoesNotExist:
        print(f"❌ Upload not found: {upload_id}")
        return Response({
            'error': 'Upload not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_upload(request, upload_id):
    """Delete an upload and its associated files"""
    print("=" * 50)
    print(f"🗑️  DELETE UPLOAD - User: {request.user.username}, Upload ID: {upload_id}")
    print("=" * 50)
    
    try:
        upload = Upload.objects.get(upload_id=upload_id, user=request.user)
        filename = upload.filename
        file_path = upload.file_path
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            print(f"🗑️  Deleted file: {file_path}")
        
        upload.delete()
        print(f"✅ Upload deleted from database: {filename}")
        
        return Response({
            'message': f'Upload "{filename}" deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Upload.DoesNotExist:
        print(f"❌ Upload not found: {upload_id}")
        return Response({
            'error': 'Upload not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Delete error: {str(e)}")
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_pdf_report(request, upload_id):
    """Download PDF report for an upload"""
    print("=" * 50)
    print(f"📥 PDF DOWNLOAD - User: {request.user.username}, Upload ID: {upload_id}")
    print("=" * 50)
    
    try:
        upload = Upload.objects.get(upload_id=upload_id, user=request.user)
        
        if not default_storage.exists(upload.file_path):
            print(f"❌ File not found in storage: {upload.file_path}")
            return Response({
                'error': 'File not found in storage'
            }, status=status.HTTP_404_NOT_FOUND)
        
        file_ext = os.path.splitext(upload.filename)[1].lower()
        file_data = default_storage.open(upload.file_path, 'rb').read()
        
        if file_ext == '.csv':
            df = pd.read_csv(io.BytesIO(file_data))
        else:
            df = pd.read_excel(io.BytesIO(file_data))
        
        numeric_df = df.select_dtypes(include=['number'])
        
        print(f"Generating PDF for file: {upload.filename}")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, 
                               topMargin=30, bottomMargin=18)
        
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = styles['Normal']
        
        title = Paragraph("Data Analysis Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        info_data = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['File Name:', upload.filename],
            ['Generated By:', request.user.username],
            ['Upload ID:', upload_id],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Dataset Overview", heading_style))
        overview_data = [
            ['Total Rows:', str(df.shape[0])],
            ['Total Columns:', str(df.shape[1])],
            ['Memory Usage:', f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"],
        ]
        
        overview_table = Table(overview_data, colWidths=[2*inch, 4*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#eff6ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dbeafe'))
        ]))
        elements.append(overview_table)
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Column Information", heading_style))
        column_data = [['Column Name', 'Data Type', 'Non-Null Count', 'Null Count']]
        
        for col in df.columns:
            non_null = df[col].count()
            null_count = df[col].isnull().sum()
            dtype = str(df[col].dtype)
            column_data.append([str(col)[:30], str(dtype)[:20], str(non_null), str(null_count)])
        
        if len(column_data) > 1:
            column_table = Table(column_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            column_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            elements.append(column_table)
        else:
            elements.append(Paragraph("No columns to display", normal_style))
        
        elements.append(PageBreak())
        
        elements.append(Paragraph("Key Highlights", heading_style))
        highlights = []
        if not numeric_df.empty:
            for col in numeric_df.columns[:3]:
                mean_val = numeric_df[col].mean()
                std_val = numeric_df[col].std()
                highlights.append(Paragraph(f"<b>{col}:</b> Mean = {mean_val:.2f}, Std Dev = {std_val:.2f}", normal_style))
        if highlights:
            for h in highlights:
                elements.append(h)
                elements.append(Spacer(1, 0.1*inch))
        elements.append(PageBreak())
        
        elements.append(Paragraph("Statistical Summary", heading_style))
        
        if not numeric_df.empty:
            stats = numeric_df.describe()
            
            stats_data = [['Statistic'] + list(numeric_df.columns[:5])]
            
            for stat in ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']:
                row = [stat]
                for col in numeric_df.columns[:5]:
                    if stat in stats.index:
                        value = stats.loc[stat, col]
                        row.append(f"{value:.2f}" if not pd.isna(value) else "N/A")
                    else:
                        row.append("N/A")
                stats_data.append(row)
            
            stats_table = Table(stats_data, colWidths=[1.2*inch] + [1.1*inch]*min(5, len(numeric_df.columns)))
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')])
            ]))
            elements.append(stats_table)
        else:
            elements.append(Paragraph("No numeric columns found for statistical analysis.", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Missing Values Analysis", heading_style))
        missing_data = [['Column', 'Missing Count', 'Missing %']]
        
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100
            if missing_count > 0:
                missing_data.append([col, str(missing_count), f"{missing_pct:.2f}%"])
        
        if len(missing_data) > 1:
            missing_table = Table(missing_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            missing_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fef2f2')])
            ]))
            elements.append(missing_table)
        else:
            elements.append(Paragraph("✓ No missing values found in the dataset.", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(PageBreak())
        elements.append(Paragraph("Distribution Analysis", heading_style))
        if not numeric_df.empty:
            dist_data = [['Column', 'Min', 'Max', 'Median', 'Q1', 'Q3']]
            for col in numeric_df.columns[:5]:
                q1 = numeric_df[col].quantile(0.25)
                median = numeric_df[col].median()
                q3 = numeric_df[col].quantile(0.75)
                min_val = numeric_df[col].min()
                max_val = numeric_df[col].max()
                dist_data.append([str(col)[:25], f"{min_val:.2f}", f"{max_val:.2f}", f"{median:.2f}", f"{q1:.2f}", f"{q3:.2f}"])
            
            if len(dist_data) > 1:
                dist_table = Table(dist_data, colWidths=[1.8*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
                dist_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')])
                ]))
                elements.append(dist_table)
        elements.append(PageBreak())
        
        if HAS_MATPLOTLIB and not numeric_df.empty:
            try:
                elements.append(Paragraph("Charts & Visualizations", heading_style))
                
                for col_idx, col in enumerate(numeric_df.columns[:3]):
                    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                    ax.plot(numeric_df[col].head(20), marker='o', linewidth=2, color=['#2563eb', '#059669', '#7c3aed'][col_idx % 3])
                    ax.set_title(f'{col} - Line Chart')
                    ax.set_xlabel('Index')
                    ax.set_ylabel('Value')
                    ax.grid(True, alpha=0.3)
                    chart_buffer = io.BytesIO()
                    plt.savefig(chart_buffer, format='png', bbox_inches='tight')
                    chart_buffer.seek(0)
                    plt.close(fig)
                    try:
                        elements.append(RLImage(chart_buffer, width=5*inch, height=2.5*inch))
                        elements.append(Spacer(1, 0.15*inch))
                    except:
                        pass
                
                fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                numeric_df.iloc[:, 0].head(12).plot(kind='bar', ax=ax, color='#2563eb')
                ax.set_title(f'{numeric_df.columns[0]} - Bar Chart')
                ax.set_xlabel('Index')
                ax.set_ylabel('Value')
                ax.tick_params(axis='x', rotation=45)
                chart_buffer = io.BytesIO()
                plt.savefig(chart_buffer, format='png', bbox_inches='tight')
                chart_buffer.seek(0)
                plt.close(fig)
                try:
                    elements.append(RLImage(chart_buffer, width=5*inch, height=2.5*inch))
                    elements.append(Spacer(1, 0.15*inch))
                except:
                    pass
                
                if len(numeric_df.columns) > 1:
                    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                    pie_data = numeric_df.iloc[:, 1].head(8)
                    ax.pie(pie_data, labels=[f'Item {i+1}' for i in range(len(pie_data))], autopct='%1.1f%%', startangle=90)
                    ax.set_title(f'{numeric_df.columns[1]} - Pie Chart')
                    chart_buffer = io.BytesIO()
                    plt.savefig(chart_buffer, format='png', bbox_inches='tight')
                    chart_buffer.seek(0)
                    plt.close(fig)
                    try:
                        elements.append(RLImage(chart_buffer, width=5*inch, height=2.5*inch))
                        elements.append(Spacer(1, 0.15*inch))
                    except:
                        pass
                
                fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                ax.hist(numeric_df.iloc[:, 0].dropna(), bins=20, color='#059669', edgecolor='black', alpha=0.7)
                ax.set_title(f'{numeric_df.columns[0]} - Distribution Histogram')
                ax.set_xlabel('Value')
                ax.set_ylabel('Frequency')
                chart_buffer = io.BytesIO()
                plt.savefig(chart_buffer, format='png', bbox_inches='tight')
                chart_buffer.seek(0)
                plt.close(fig)
                try:
                    elements.append(RLImage(chart_buffer, width=5*inch, height=2.5*inch))
                    elements.append(Spacer(1, 0.15*inch))
                except:
                    pass
                
                if len(numeric_df.columns) > 1:
                    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                    ax.scatter(numeric_df.iloc[:, 0].head(50), numeric_df.iloc[:, 1].head(50), alpha=0.6, s=50, color='#7c3aed')
                    ax.set_title(f'{numeric_df.columns[0]} vs {numeric_df.columns[1]} - Scatter Plot')
                    ax.set_xlabel(numeric_df.columns[0])
                    ax.set_ylabel(numeric_df.columns[1])
                    ax.grid(True, alpha=0.3)
                    chart_buffer = io.BytesIO()
                    plt.savefig(chart_buffer, format='png', bbox_inches='tight')
                    chart_buffer.seek(0)
                    plt.close(fig)
                    try:
                        elements.append(RLImage(chart_buffer, width=5*inch, height=2.5*inch))
                        elements.append(Spacer(1, 0.15*inch))
                    except:
                        pass
                
                if len(numeric_df.columns) > 1:
                    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                    x_vals = range(min(15, len(numeric_df)))
                    ax.bar(x_vals, numeric_df.iloc[:15, 0], alpha=0.7, color='#2563eb', label=numeric_df.columns[0])
                    ax2 = ax.twinx()
                    ax2.plot(x_vals, numeric_df.iloc[:15, 1], color='#dc2626', marker='o', linewidth=2, label=numeric_df.columns[1])
                    ax.set_xlabel('Index')
                    ax.set_ylabel(numeric_df.columns[0], color='#2563eb')
                    ax2.set_ylabel(numeric_df.columns[1], color='#dc2626')
                    ax.set_title('Combined Chart - Multiple Parameters')
                    ax.tick_params(axis='y', labelcolor='#2563eb')
                    ax2.tick_params(axis='y', labelcolor='#dc2626')
                    ax.legend(loc='upper left')
                    chart_buffer = io.BytesIO()
                    plt.savefig(chart_buffer, format='png', bbox_inches='tight')
                    chart_buffer.seek(0)
                    plt.close(fig)
                    try:
                        elements.append(RLImage(chart_buffer, width=5*inch, height=2.5*inch))
                        elements.append(Spacer(1, 0.15*inch))
                    except:
                        pass
                
                fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                box_data = [numeric_df[col].dropna() for col in numeric_df.columns[:3]]
                ax.boxplot(box_data, labels=numeric_df.columns[:3])
                ax.set_title('Statistical Box Plot')
                ax.set_ylabel('Value')
                chart_buffer = io.BytesIO()
                plt.savefig(chart_buffer, format='png', bbox_inches='tight')
                chart_buffer.seek(0)
                plt.close(fig)
                try:
                    elements.append(RLImage(chart_buffer, width=5*inch, height=2.5*inch))
                    elements.append(Spacer(1, 0.15*inch))
                except:
                    pass
                
                elements.append(PageBreak())
            except Exception as chart_err:
                print(f"Warning: Could not generate charts: {chart_err}")
                traceback.print_exc()
                elements.append(Paragraph("Charts section generated", normal_style))
        
        elements.append(Paragraph("Data Sample (First 15 Rows)", heading_style))
        
        sample_df = df.head(15)
        sample_data = [[str(col)[:15] for col in sample_df.columns]]
        
        for idx, row in sample_df.iterrows():
            sample_data.append([str(val)[:15] for val in row.values])
        
        num_cols = len(sample_df.columns)
        col_width = 6.5 * inch / max(num_cols, 1)
        
        sample_table = Table(sample_data, colWidths=[col_width] * num_cols)
        sample_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf5ff')])
        ]))
        elements.append(sample_table)
        
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER
        )
        footer_text = f"Generated by Chemizer Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elements.append(Paragraph(footer_text, footer_style))
        
        doc.build(elements)
        
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="analysis_report_{upload_id}.pdf"'
        
        print(f"✅ PDF generated successfully for upload_id: {upload_id}")
        
        return response
        
    except Upload.DoesNotExist:
        print(f"❌ Upload not found: {upload_id}")
        return Response({
            'error': 'Upload not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ PDF generation error: {str(e)}")
        traceback.print_exc()
        return Response({
            'error': f'PDF generation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_delete_uploads(request):
    """Delete multiple uploads at once"""
    try:
        upload_ids = request.data.get('upload_ids', [])
        if not upload_ids:
            return Response({'error': 'No upload IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploads = Upload.objects.filter(upload_id__in=upload_ids, user=request.user)
        for upload in uploads:
            if default_storage.exists(upload.file_path):
                default_storage.delete(upload.file_path)
            upload.delete()
        
        return Response({'message': f'Deleted {len(uploads)} uploads'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_all_data(request):
    """Export all uploads as CSV"""
    try:
        uploads = Upload.objects.filter(user=request.user).order_by('-upload_date')
        
        export_data = []
        for upload in uploads:
            export_data.append({
                'filename': upload.filename,
                'upload_date': upload.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                'rows': upload.rows,
                'columns': upload.columns,
                'file_size_bytes': upload.file_size,
            })
        
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="all_uploads_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.DictWriter(response, fieldnames=['filename', 'upload_date', 'rows', 'columns', 'file_size_bytes'])
        writer.writeheader()
        writer.writerows(export_data)
        
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_all_data(request):
    """Delete all uploads for the user"""
    try:
        uploads = Upload.objects.filter(user=request.user)
        count = uploads.count()
        
        for upload in uploads:
            if default_storage.exists(upload.file_path):
                default_storage.delete(upload.file_path)
            upload.delete()
        
        return Response({'message': f'Deleted {count} uploads and all associated data'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)