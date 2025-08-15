from celery import shared_task
import subprocess
import joblib
import os
import json
import pandas as pd
from compliance_scanner.models import IPAddress, ComplianceRule, ScanResult

from .utils import validate_compliance


from .models import IPAddress, ComplianceRule, ComplianceStatus

@shared_task
def update_all_compliance():
    """
    Task to update compliance status for all IP addresses.
    """
    ip_addresses = IPAddress.objects.all()
    frameworks = [choice[0] for choice in ComplianceStatus.FRAMEWORK_CHOICES]

    for ip_address in ip_addresses:
        for framework in frameworks:
            validate_compliance(ip_address, framework)


# Load the model once when the worker starts
model_path = os.path.join(os.path.dirname(__file__), 'ml', 'model.pkl')

try:
    model = joblib.load(model_path)
except FileNotFoundError:
    print(f"Model file not found at {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")


def parse_nmap_output(output):
    """
    Parse the Nmap output and return vulnerabilities in a structured format.
    This example assumes we are looking for certain keywords or patterns in the Nmap output.
    Modify based on the actual output of the Nmap scan.
    """
    vulnerabilities = []
    for line in output.splitlines():
        if "VULNERABLE" in line:  # Change this based on your output pattern
            vulnerabilities.append({
                'description': line.strip(),
                'severity': 'High'  # Modify as needed based on analysis of output
            })
    return vulnerabilities


@shared_task
def run_nmap_scan(ip):
    """
    Run an Nmap scan on the provided IP address and check for vulnerabilities
    against compliance rules.
    """
    result = subprocess.run(["nmap", "-sV", ip], capture_output=True, text=True)
    vulnerabilities = parse_nmap_output(result.stdout)

    # Check vulnerabilities against compliance rules and store results in the database
    for vulnerability in vulnerabilities:
        matching_rules = ComplianceRule.objects.filter(description__icontains=vulnerability['description'])
        for rule in matching_rules:
            # Create a new ScanResult for each matching rule
            ip_address, created = IPAddress.objects.get_or_create(address=ip)
            ScanResult.objects.create(
                ip_address=ip_address,
                vulnerability=vulnerability['description'],
                risk_level=rule.severity  # Assuming rules have severity attribute
            )

    return result.stdout


@shared_task
def detect_anomalies(data):
    """
    Detect anomalies using the pre-trained ML model.
    """
    if model:
        try:
            prediction = model.predict([data])  # Assuming data is in the correct format for prediction
            return prediction.tolist()  # Return the prediction as a list
        except Exception as e:
            print(f"Error during anomaly detection: {e}")
            return None
    else:
        return "Model is not loaded."


@shared_task
def parse_nvd_data(file_path):
    """
    Parse the NVD JSON data and extract relevant vulnerability information.
    Save the parsed data into a CSV file.
    """
    # Load the JSON data
    with open(file_path) as file:
        nvd_data = json.load(file)

    # Initialize a DataFrame to store vulnerabilities
    vulnerabilities_df = pd.DataFrame()

    # Extract the relevant fields
    for entry in nvd_data['CVE_Items']:
        cve_id = entry['cve']['CVE_data_meta']['ID']
        description = entry['cve']['description']['description_data'][0]['value']
        
        # Extract CVSS severity score (if available)
        try:
            cvss_score = entry['impact']['baseMetricV2']['severity']
        except KeyError:
            cvss_score = 'N/A'

        # Extract affected software (CPE)
        affected_software = []
        for node in entry['configurations']['nodes']:
            for cpe in node.get('cpe_match', []):
                affected_software.append(cpe['cpe23Uri'])

        vulnerabilities_df = vulnerabilities_df.append({
            'CVE ID': cve_id,
            'Description': description,
            'CVSS Severity': cvss_score,
            'Affected Software': ', '.join(affected_software)
        }, ignore_index=True)

    # Save the parsed data into a CSV file
    vulnerabilities_df.to_csv('nvd_vulnerabilities_2024.csv', index=False)
    return "Data parsing and CSV export completed"
