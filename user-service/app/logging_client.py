import os
import requests

LOGGING_SERVICE_URL = os.getenv("LOGGING_SERVICE_URL", "http://logging-service:8000/logs/")

def send_audit_log(company_id, user_id, action, details=None):
    payload = {
        "company_id": company_id,
        "user_id": str(user_id) if user_id else None,
        "action": action,
        "details": details or {},
    }
    try:
        resp = requests.post(LOGGING_SERVICE_URL, json=payload, timeout=2)
        resp.raise_for_status()
    except Exception as e:
        print(f"[AuditLog] Failed to send log to logging-service: {e}") 