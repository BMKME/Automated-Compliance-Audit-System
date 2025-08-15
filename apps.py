# compliance_audit_system/apps.py

from django.apps import AppConfig

class ComplianceAuditSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Add this line
    name = 'compliance_audit_system'