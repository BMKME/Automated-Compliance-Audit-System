ashCopy#!/bin/bash

# Start Redis
redis-server &

# Start Celery worker
celery -A compliance_audit_system worker -l info &

# Start Celery beat
celery -A compliance_audit_system beat -l info &

# Start Django development server
python manage.py runserver


Make this file executable:
bashCopychmod +x start_services.sh

