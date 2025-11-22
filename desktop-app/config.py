# ============================================
# API Configuration
# ============================================
import os
from pathlib import Path

try:
	from dotenv import load_dotenv
	env_path = Path(__file__).resolve().parent / ".env"
	if env_path.exists():
		load_dotenv(env_path)
except Exception:
	pass

# API base URL used by the desktop client.
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

DEBUG = str(os.getenv("DEBUG", "True")).lower() in ("1", "true", "yes")
# ============================================
# Google OAuth Configuration
# ============================================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
