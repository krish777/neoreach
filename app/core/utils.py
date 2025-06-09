import json
from datetime import datetime
from typing import Dict, Any
import hashlib

def generate_id(input_data: Dict[str, Any]) -> str:
    """Deterministic ID generation for Neo4j nodes"""
    input_str = json.dumps(input_data, sort_keys=True)
    return hashlib.md5(input_str.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[-1]

def log_execution(action: str, metadata: Dict[str, Any]):
    """Structured logging"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "metadata": metadata,
        "system": "neoreach"
    }

def safe_json_loads(json_str: str) -> Dict:
    """Graceful JSON parsing"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}