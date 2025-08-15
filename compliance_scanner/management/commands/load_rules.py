import json
from django.core.management.base import BaseCommand
from compliance_scanner.models import ComplianceRule

class Command(BaseCommand):
    help = "Load predefined compliance rules into the database"

    def handle(self, *args, **kwargs):
        try:
            with open('compliance_scanner/compliance_rules.json', 'r') as file:
                rules = json.load(file)
                for rule in rules:
                    ComplianceRule.objects.get_or_create(
                        rule_name=rule['rule_name'],
                        description=rule['description'],
                        framework=rule['framework']
                    )
            self.stdout.write(self.style.SUCCESS("Compliance rules loaded successfully!"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("File 'compliance_rules.json' not found."))

