from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('change-password/', views.change_password, name='change-password'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path('google/', views.google_login, name='google-login'),
    path('profile/', views.get_profile, name='get-profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('profile/delete/', views.delete_account, name='delete-account'),
    path('upload/', views.upload_file, name='upload-file'),
    path('uploads/history/', views.get_upload_history, name='upload-history'),
    path('uploads/<str:upload_id>/', views.get_upload_detail, name='upload-detail'),  
    path('uploads/<str:upload_id>/delete/', views.delete_upload, name='delete-upload'),  
    path('reports/download/<str:upload_id>/', views.download_pdf_report, name='download-report'),
    path('upload-history/', views.upload_history, name='upload-history-desktop'),  
    path('uploads/bulk-delete/', views.bulk_delete_uploads, name='bulk-delete-uploads'),
    path('data/download-all/', views.download_all_data, name='download-all-data'),
    path('data/delete-all/', views.delete_all_data, name='delete-all-data'),
]