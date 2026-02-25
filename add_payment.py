"""Example: create a single payment (PSID or DQRC or SQRC_RETAIL)

Edit BASE_URL, USERNAME, PASSWORD and CHANNEL_ID before running.
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

    # Example: PSID with amount
    payment_body = {
        "payment": {
            "title": "Demo Payment",
            "identifier": "DEMO-12345",
            "dueDate": "2026-02-28",
            "amount": "100",
            "amountAfterDueDate": "110"
        }
    }

    # generationTypes can be PSID, DQRC, SQRC_RETAIL, SQRC_BILL, SQRC_RETAIL
    resp = client.add_payment(token=token, channel_id=CHANNEL_ID, payment=payment_body, generation_type="PSID")
    print("Add payment response:\n", resp)

