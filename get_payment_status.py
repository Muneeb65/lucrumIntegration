"""Example: fetch a payment by PSID using /integration/payment/{paymentId}

Edit BASE_URL, USERNAME, PASSWORD and CHANNEL_ID before running.
Set PAYMENT_ID to the PSID you want to look up.
"""
from api_client import AsaanBillClient
import os

BASE_URL = os.environ.get("ASAAN_BASE_URL", "https://mypaymenthub-stg.evampsaanga.com")
USERNAME = os.environ.get("ASAAN_USERNAME", "abc")
PASSWORD = os.environ.get("ASAAN_PASSWORD", "abc")
CHANNEL_ID = os.environ.get("ASAAN_CHANNEL_ID", "79")
PAYMENT_ID = os.environ.get("ASAAN_PAYMENT_ID", "100139100100154854584585")


def main():
    client = AsaanBillClient(BASE_URL, USERNAME)
    login_resp = client.login(PASSWORD)
    token = login_resp.get("data", {}).get("token")
    if not token:
        print("Login failed or token missing:", login_resp)
        return

    resp = client.get_payment_by_id(token=token, channel_id=CHANNEL_ID, payment_id=PAYMENT_ID)
    print("Get payment response:\n", resp)

