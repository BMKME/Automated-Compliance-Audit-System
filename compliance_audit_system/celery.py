import django
django.setup()

from compliance_scanner.models import NmapScan, NiktoScan, ComplianceStatus


import os
import joblib
import logging
from celery import Celery, shared_task
from compliance_scanner.models import NmapScan, NiktoScan, ComplianceStatus
import subprocess

# Set up the Django settings for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compliance_audit_system.settings')

# Initialize the Celery app
app = Celery('compliance_audit_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Logger setup
logger = logging.getLogger(__name__)

# Model path
MODEL_PATH = '/home/dodo/compliance_audit_system/compliance_scanner/ml/model.pkl'

# Load the pre-trained model
try:
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
except FileNotFoundError:
    model = None
    logger.warning(f"Model file not found at {MODEL_PATH}.")
except Exception as e:
    model = None
    logger.error(f"Error loading model: {e}")

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@shared_task
def predict_vulnerabilities(data):
    """Predict vulnerabilities or anomalies based on the pre-trained model."""
    if model is None:
        logger.error("Model not available. Prediction cannot be performed.")
        return {"error": "Model not available."}
    try:
        prediction = model.predict([data])  # Assuming 'data' is preprocessed correctly
        logger.info("Prediction performed successfully.")
        return prediction.tolist()
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return {"error": f"Prediction failed: {str(e)}"}

@shared_task
def run_nmap_scan(target):
    """Run an Nmap scan."""
    scan = NmapScan.objects.create(target=target, status="Running")
    try:
        result = subprocess.run(['nmap', target], capture_output=True, text=True)
        scan.status = "Complete"
        scan.save()
        return result.stdout
    except Exception as e:
        scan.status = "Failed"
        scan.save()
        logger.error(f"Nmap scan failed: {e}")
        return {"error": f"Nmap scan failed: {str(e)}"}

@shared_task
def run_nikto_scan(target):
    """Run a Nikto scan."""
    scan = NiktoScan.objects.create(url=target, status="Running")
    try:
        result = subprocess.run(['nikto', '-h', target], capture_output=True, text=True)
        scan.status = "Complete"
        scan.save()
        return result.stdout
    except Exception as e:
        scan.status = "Failed"
        scan.save()
        logger.error(f"Nikto scan failed: {e}")
        return {"error": f"Nikto scan failed: {str(e)}"}
