from django.contrib import admin
from django.urls import path, include
from .views import login_page, register_page, dashboard
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('analysis.urls')),   

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('text-checker/', TemplateView.as_view(template_name='text_checker.html'), name='text-checker'),
    path('file-checker/', TemplateView.as_view(template_name='file_checker.html'), name='file-checker'),
    path('reports/', TemplateView.as_view(template_name='reports.html'), name='reports'),
]

