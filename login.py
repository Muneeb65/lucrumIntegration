"""Example: login to AsaanBill integration and print token/channel info.

Edit USERNAME, PASSWORD and BASE_URL with your staging credentials.
"""
from api_client import AsaanBillClient
import os

# === Edit these values ===
# Use provided defaults (can be overridden with environment variables)
BASE_URL = os.environ.get("ASAAN_BASE_URL", "https://mypaymenthub-stg.evampsaanga.com")
USERNAME = os.environ.get("ASAAN_USERNAME", "abc")
PASSWORD = os.environ.get("ASAAN_PASSWORD", "abc")

def main():
    client = AsaanBillClient(BASE_URL, USERNAME)
    resp = client.login(PASSWORD)
    print("Login response:\n", resp)
