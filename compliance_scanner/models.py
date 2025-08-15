from django.db import models
from django.utils.timezone import now

class IPAddress(models.Model):
    address = models.GenericIPAddressField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = "IP Addresses"

class ComplianceRule(models.Model):
    # Remove hardcoded FRAMEWORK_CHOICES for dynamic framework support
    rule_name = models.CharField(max_length=255)
    description = models.TextField()
    framework = models.CharField(max_length=100)  # Increased length for flexibility
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rule_name} ({self.framework})"

    class Meta:
        verbose_name = "Compliance Rule"
        verbose_name_plural = "Compliance Rules"
        ordering = ['framework', 'rule_name']

class ScanResult(models.Model):
    RISK_LEVEL_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    vulnerability = models.TextField()
    risk_level = models.CharField(max_length=50, choices=RISK_LEVEL_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.ip_address} - {self.risk_level}"

    class Meta:
        verbose_name = "Scan Result"
        verbose_name_plural = "Scan Results"
        ordering = ['-timestamp']

class ComplianceStatus(models.Model):
    # Remove hardcoded FRAMEWORK_CHOICES for dynamic framework support
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    framework = models.CharField(max_length=100)  # Increased length for flexibility
    compliance_status = models.CharField(max_length=50, default="Non-Compliant")
    last_checked = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.framework} Compliance - {self.ip_address.address}"

    class Meta:
        verbose_name = "Compliance Status"
        verbose_name_plural = "Compliance Statuses"
        ordering = ['ip_address', 'framework']

    def audit_active_directory(self):
        """Audit Active Directory for users and their groups."""
        # Properly indented code block
        pass  # Replace with actual implementation

class NmapScan(models.Model):
    target = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nmap Scan - {self.target}"

    class Meta:
        verbose_name = "Nmap Scan"
        verbose_name_plural = "Nmap Scans"
        ordering = ['-created_at']

class NiktoScan(models.Model):
    url = models.URLField()
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nikto Scan - {self.url}"

    class Meta:
        verbose_name = "Nikto Scan"
        verbose_name_plural = "Nikto Scans"
        ordering = ['-created_at']

class AIPredictions(models.Model):
    input_data = models.TextField()
    output_data = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Prediction - {self.input_data[:30]}"

    class Meta:
        verbose_name = "AI Prediction"
        verbose_name_plural = "AI Predictions"
        ordering = ['-created_at']

        