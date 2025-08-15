from django.core.management.base import BaseCommand
from compliance_audit_system.models import IPAddress, ComplianceStatus

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        data = [
            {'ip_address': '192.168.1.1', 'description': 'Main Server', 'compliance': {'framework': 'NIST', 'compliance_status': 'Compliant'}},
            {'ip_address': '192.168.1.2', 'description': 'Backup Server', 'compliance': {'framework': 'ISO27001', 'compliance_status': 'Non-Compliant'}},
            {'ip_address': '192.168.1.3', 'description': 'Web Server', 'compliance': {'framework': 'CMA', 'compliance_status': 'Compliant'}},
            {'ip_address': '192.168.1.4', 'description': 'Database Server', 'compliance': {'framework': 'SOC2', 'compliance_status': 'Non-Compliant'}},
            {'ip_address': '192.168.1.5', 'description': 'Mail Server', 'compliance': {'framework': 'DPPA', 'compliance_status': 'Compliant'}},
            {'ip_address': '192.168.1.6', 'description': 'FTP Server', 'compliance': {'framework': 'NIST', 'compliance_status': 'Compliant'}},
            {'ip_address': '192.168.1.7', 'description': 'Application Server', 'compliance': {'framework': 'COBIT', 'compliance_status': 'Non-Compliant'}},
            {'ip_address': '192.168.1.8', 'description': 'Gateway', 'compliance': {'framework': 'ISO27001', 'compliance_status': 'Compliant'}},
            {'ip_address': '192.168.1.9', 'description': 'Firewall', 'compliance': {'framework': 'NIST', 'compliance_status': 'Non-Compliant'}},
            {'ip_address': '192.168.1.10', 'description': 'Proxy Server', 'compliance': {'framework': 'CMA', 'compliance_status': 'Compliant'}},
            {'ip_address': '192.168.1.11', 'description': 'Load Balancer', 'compliance': {'framework': 'SOC2', 'compliance_status': 'Non-Compliant'}},
            {'ip_address': '192.168.1.12', 'description': 'DNS Server', 'compliance': {'framework': 'DPPA', 'compliance_status': 'Compliant'}},
            {'ip_address': 'isbatuniversity.ac.ug', 'description': 'ISBAT University Website', 'compliance': {'framework': 'ISO27001', 'compliance_status': 'Compliant'}},
            {'ip_address': 'localhost', 'description': 'Localhost Server', 'compliance': {'framework': 'NIST', 'compliance_status': 'Non-Compliant'}}
        ]

        for entry in data:
            try:
                # Create or update the IP address entry
                ip, created = IPAddress.objects.get_or_create(
                    address=entry['ip_address'],
                    defaults={'description': entry['description']}
                )

                # Update description if the IP already exists
                if not created:
                    ip.description = entry['description']
                    ip.save(update_fields=['description'])
                    self.stdout.write(self.style.WARNING(f"Updated IP: {ip.address}"))

                # Create or update compliance status
                compliance_data = entry['compliance']
                ComplianceStatus.objects.update_or_create(
                    ip_address=ip,
                    framework=compliance_data['framework'],
                    defaults={'compliance_status': compliance_data['compliance_status']}
                )

                self.stdout.write(self.style.SUCCESS(f"Processed IP: {ip.address}"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing IP {entry['ip_address']}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully'))