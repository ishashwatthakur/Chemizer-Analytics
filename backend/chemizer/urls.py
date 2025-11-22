from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),      
    path('api/reports/download/<str:upload_id>/', accounts_views.download_pdf_report, name='download-report'),
    path('api/reports/download-all/', accounts_views.download_all_data, name='download-all-data'),
    path('accounts/', include('allauth.urls')),       
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)