# compliance_audit_system/urls.py

from django.contrib import admin
from django.urls import path
from . import views as core_views  # Ensure this file exists
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]

urlpatterns = [
    # Other URL patterns
    path('generate-excel/', views.generate_excel, name='generate_excel'),
]

urlpatterns = [
    path('nmap_scan/', views.run_nmap, name='run_nmap'),
    # other paths
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.landing_page, name='landing_page'),
    path('dashboard/', core_views.dashboard_view, name='dashboard'),
    path('compliance_scanner/', core_views.compliance_scanner, name='compliance_scanner'),
    path('nmap/', core_views.run_nmap, name='run_nmap'),
    path('nikto/', core_views.run_nikto, name='run_nikto'),
    path('ad-audit/', core_views.audit_active_directory, name='ad_audit'),
    path('monitor-processes/', core_views.monitor_rogue_processes, name='monitor_processes'),
    path('generate-pdf/', core_views.generate_pdf, name='generate_pdf'),
    path('generate-excel/', core_views.generate_excel, name='generate_excel'),
    path('compliance/', core_views.check_compliance, name='check_compliance'),
    path('compliance_dashboard/', core_views.compliance_dashboard, name='compliance_dashboard'),
    path('get_compliance_data/', core_views.get_compliance_data, name='get_compliance_data'),
]