from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import subprocess
import plotly.express as px
import pandas as pd
from reportlab.pdfgen import canvas
from ldap3 import Server, Connection
import psutil
from .models import ComplianceStatus
from django.conf import settings
from reportlab.lib.pagesizes import letter

def compliance_dashboard(request):
    """Render the compliance dashboard with a bar chart of compliance status."""
    # Fetch data from the ComplianceStatus model
    compliance_statuses = ComplianceStatus.objects.all()
    # Debug: Print the queryset
    print(f"Compliance statuses: {compliance_statuses}")
    
    # Convert the queryset to a DataFrame
    data = pd.DataFrame(list(compliance_statuses.values('ip_address__address', 'compliance_status', 'framework')))
    # Debug: Print the DataFrame
    print(f"DataFrame: {data}")

    # Rename columns to match expected names
    data.rename(columns={'ip_address__address': 'ip_address'}, inplace=True)

    # Ensure the DataFrame has the necessary columns
    if not all(column in data.columns for column in ['ip_address', 'compliance_status', 'framework']):
        return render(request, 'compliance_dashboard.html', {'error': 'Required columns are missing from the data.'})

    # Create the bar chart
    fig = px.bar(data, x='ip_address', y='compliance_status', color='framework', title='Compliance Status by Framework')
    graph_html = fig.to_html(full_html=False)

    # Render the template with the bar chart
    return render(request, 'compliance_dashboard.html', {"graph": graph_html})

def landing_page(request):
    """Render the landing page."""
    return render(request, 'landing_page.html')

def dashboard_view(request):
    """Render the compliance dashboard with a Plotly bar chart."""
    compliance_data = {
        "Standard": ["ISO 27001", "NIST", "DPPA", "CMA"],
        "Compliant Assets": [20, 15, 10, 8],
        "Non-Compliant Assets": [5, 10, 12, 6],
    }
    fig = px.bar(compliance_data, x="Standard", y=["Compliant Assets", "Non-Compliant Assets"], barmode="group")
    graph_html = fig.to_html(full_html=False)
    return render(request, 'dashboard.html', {"graph": graph_html})

def get_compliance_data(request):
    """Fetch compliance data and return as JSON for Plotly."""
    # Fetch data from the ComplianceStatus model
    compliance_statuses = ComplianceStatus.objects.all()
    
    # Convert the queryset to a DataFrame
    data = pd.DataFrame(list(compliance_statuses.values('ip_address__address', 'compliance_status', 'framework')))
    
    # Debug: Print the DataFrame and its columns
    print("DataFrame contents:\n", data)
    print("DataFrame columns:", data.columns)

    # Rename columns to match expected names
    data.rename(columns={'ip_address__address': 'ip_address'}, inplace=True)
    
    # Debug: Print the DataFrame after renaming columns
    print("DataFrame after renaming columns:\n", data)
    
    # Ensure the DataFrame has the necessary columns
    if not all(column in data.columns for column in ['ip_address', 'compliance_status', 'framework']):
        return JsonResponse({'error': 'Required columns are missing from the data.'}, status=400)

    # Create the bar chart
    fig = px.bar(data, x='ip_address', y='compliance_status', color='framework', title='Compliance Status by Framework')
    return JsonResponse(fig.to_json(), safe=False)

def compliance_scanner(request):
    """Render the compliance scanner dashboard with a Plotly chart."""
    data = {
        "Category": ["Compliance", "Threat Detection", "Audit Progress"],
        "Value": [80, 70, 90]
    }
    fig = px.bar(data, x="Category", y="Value", title="Audit Overview")
    graph_html = fig.to_html(full_html=False)
    return render(request, 'compliance_scanner.html', {'graph_html': graph_html})

def run_nmap(request):
    """Run an Nmap scan on the provided target."""
    if request.method == 'POST':
        target = request.POST.get('target')
        command = f"nmap {target}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return render(request, 'scan_results.html', {'output': result.stdout})
    return render(request, 'nmap_scan.html')

def run_nikto(request):
    """Run a Nikto scan on the provided target."""
    if request.method == 'POST':
        target = request.POST.get('target')
        command = f"nikto -h {target}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return render(request, 'scan_results.html', {'output': result.stdout})
    return render(request, 'nikto_scan.html')

def audit_active_directory(request):
    """Audit Active Directory for users and their groups."""
    try:
        server = Server(settings.LDAP_SERVER)  # Use settings for sensitive data
        conn = Connection(server, user=settings.LDAP_USER, password=settings.LDAP_PASSWORD, auto_bind=True)
        conn.search('dc=example,dc=com', '(objectclass=person)', attributes=['cn', 'memberOf'])
        data = conn.entries
    except Exception as e:
        data = []  # Initialize data to an empty list in case of error
        return render(request, 'ad_audit_results.html', {'error': str(e), 'data': data})
    return render(request, 'ad_audit_results.html', {'data': data})

def monitor_rogue_processes(request):
    """Monitor the system for rogue processes."""
    rogue_processes = []
    for process in psutil.process_iter(['pid', 'name']):
        if 'suspicious_process' in process.info['name']:  # Define suspicious process names
            rogue_processes.append(process.info)
    return render(request, 'rogue_processes.html', {'processes': rogue_processes})




def generate_pdf(request):
    """Generate a PDF audit report."""
    # Create a HttpResponse object with the appropriate PDF header
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="audit_report.pdf"'
    
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    
    # Set up the PDF page
    width, height = letter
    p.setFont("Helvetica", 12)
    
    # Add a title
    p.drawString(100, height - 50, "Audit Report")
    
    # Add some content
    p.drawString(100, height - 100, "Introduction")
    p.drawString(100, height - 120, "This is the audit report generated for the compliance system.")
    
    p.drawString(100, height - 160, "Problem Statement")
    p.drawString(100, height - 180, "Describe the problem your project aims to solve.")
    
    p.drawString(100, height - 220, "Main Objective")
    p.drawString(100, height - 240, "State the main objective of your project.")
    
    p.drawString(100, height - 280, "Specific Objectives")
    p.drawString(100, height - 300, "List the specific objectives of your project.")
    
    p.drawString(100, height - 340, "Research Questions")
    p.drawString(100, height - 360, "List the research questions you aim to answer.")
    
    p.drawString(100, height - 400, "Literature Review")
    p.drawString(100, height - 420, "Summarize the existing literature related to your project.")
    
    p.drawString(100, height - 460, "Methodology")
    p.drawString(100, height - 480, "Describe the methodology you used in your project.")
    
    p.drawString(100, height - 520, "Design and Implementation")
    p.drawString(100, height - 540, "Explain the design and implementation of your project.")
    
    p.drawString(100, height - 580, "Demonstration")
    p.drawString(100, height - 600, "Show a demonstration of your project.")
    
    p.drawString(100, height - 640, "Conclusion")
    p.drawString(100, height - 660, "Summarize the key findings and conclusions of your project.")
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response

def generate_excel(request):
    """Generate an Excel audit report."""
    data = {
        'Category': ['Compliance', 'Threat Detection'],
        'Value': [80, 70]
    }
    df = pd.DataFrame(data)
    
    # Create a HttpResponse object with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="audit_report.xlsx"'
    
    # Use the to_excel function to write the DataFrame to the Excel response
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response

def check_compliance(request):
    """Check compliance for a specific standard."""
    if request.method == 'POST':
        standard = request.POST.get('standard')
        issues = check_compliance_issues(standard)
        return render(request, 'compliance_issues.html', {'issues': issues})
    return render(request, 'compliance_check.html')

def check_compliance_issues(standard):
    """Return a list of compliance issues for a given standard."""
    issues = []
    if standard == "ISO 27001":
        issues.append("Missing encryption on database.")
    elif standard == "NIST":
        issues.append("Firewall rules are not comprehensive.")
    elif standard == "DPPA":
        issues.append("Lack of explicit user consent for data collection.")
    elif standard == "CMA":
        issues.append("Unauthorized access detected.")
    elif standard == "SOC 2":
        issues.append("Weak password policies.")
    return issues