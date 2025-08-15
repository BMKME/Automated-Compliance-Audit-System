# compliance_scanner/apps.py

from django.apps import AppConfig

class ComplianceScannerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Add this line
    name = 'compliance_scanner'