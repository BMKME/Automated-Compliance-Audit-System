from django.contrib import admin
from .models import AIPredictions, NiktoScan, NmapScan, ComplianceStatus

admin.site.site_header = 'JAD Administration'  # Changes the header
admin.site.site_title = 'JAD Admin Portal'    # Changes the browser tab title
admin.site.index_title = 'Welcome to JAD Administration'  # Changes the index page title

# Registering all models to appear in the admin interface
@admin.register(NmapScan)
class NmapScanAdmin(admin.ModelAdmin):
    list_display = ['target', 'created_at', 'status']  # Adjust fields based on your model
    list_filter = ['status', 'created_at']
    search_fields = ['target']
    date_hierarchy = 'created_at'

@admin.register(NiktoScan)
class NiktoScanAdmin(admin.ModelAdmin):
    list_display = ['url', 'created_at', 'status']  # Adjust fields based on your model
    list_filter = ['status', 'created_at']
    search_fields = ['url']
    date_hierarchy = 'created_at'

@admin.register(ComplianceStatus)
class ComplianceStatusAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'framework', 'compliance_status']  # Adjust fields based on your model
    list_filter = ['framework', 'compliance_status']
    search_fields = ['ip_address__address']  # Assuming ip_address is a ForeignKey field

@admin.register(AIPredictions)
class AIPredictionsAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'output_data']  # Adjust fields based on your model
    list_filter = ['created_at']
    date_hierarchy = 'created_at'