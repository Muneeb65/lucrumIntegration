""" AsaanBill integration client using only the Python standard library.

This client provides a few helper methods: login, add_payment, add_bulk_payments,
get_payment_by_id and search_by_psid.

It's intentionally simple and synchronous.
"""
from typing import Optional, Dict, Any
import json
import urllib.request
import urllib.parse
import urllib.error


class AsaanBillClient:
    def __init__(self, base_url: str, username: str):
        # Ensure base_url points to the /integration path (guide uses base + /integration)
        if not base_url.endswith("/integration"):
            base_url = base_url.rstrip("/") + "/integration"
        self.base_url = base_url.rstrip("/")
        self.username = username

    def _request(self, method: str, path: str, token: Optional[str] = None, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, body: Optional[dict] = None, timeout: int = 15) -> dict:
        url = self.base_url + path
        if params:
            query = urllib.parse.urlencode(params)
            url = url + "?" + query

        data = None
        req_headers = {
            "Content-Type": "application/json",
        }
        if headers:
            req_headers.update(headers)
        if token:
            # x-auth-ph-key is the token header required by the API
            req_headers["x-auth-ph-key"] = token
        if self.username:
            req_headers["username"] = self.username

        if body is not None:
            data = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(url, data=data, method=method, headers=req_headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                if not raw:
                    return {}
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            try:
                raw = e.read().decode("utf-8")
                return json.loads(raw)
            except Exception:
                return {"error": str(e), "status": e.code}
        except Exception as e:
            return {"error": str(e)}

    def login(self, password: str) -> Dict[str, Any]:
        """Call POST /integration/login with header `username` and JSON body {"password": "..."}

        Returns parsed JSON response from the server.
        """
        # base_url is expected to include the /integration suffix (per guide).
        # construct the relative path under the provided base_url
        path = "/login"
        body = {"password": password}
        # username is provided in header by _request
        return self._request("POST", path, body=body)

    def add_payment(self, token: str, channel_id: str, payment: dict, generation_type: Optional[str] = None) -> dict:
        """Call POST /integration/add to create a payment.

        - token: token received from login
        - channel_id: channel-id header (string)
        - payment: payment dict as per API (key "payment" mapping)
        - generation_type: optional query parameter `generationTypes` with values like PSID, DQRC, SQRC_RETAIL, SQRC_BILL, SQRC_RETAIL
        """
        path = "/add"
        headers = {"channel-id": str(channel_id)}
        params = {"generationTypes": generation_type} if generation_type else None
        return self._request("POST", path, token=token, headers=headers, params=params, body=payment)

    def add_bulk(self, token: str, channel_id: str, payments: dict, content_type: str = "JSON") -> dict:
        """Call POST /integration/add-bulk with `payments` body.

        payments should be a dict: {"payments": [ {..}, {...} ] }
        Add header channel-id and a query param contentType=JSON
        """
        path = "/add-bulk"
        headers = {"channel-id": str(channel_id)}
        params = {"contentType": content_type}
        return self._request("POST", path, token=token, headers=headers, params=params, body=payments)

    def get_payment_by_id(self, token: str, channel_id: str, payment_id: str) -> dict:
        path = f"/payment/{urllib.parse.quote(payment_id)}"
        headers = {"channel-id": str(channel_id)}
        return self._request("GET", path, token=token, headers=headers)

    def search_by_psid(self, token: str, channel_id: str, psid: str, pageNo: int = 0, pageSize: int = 100) -> dict:
        path = f"/search/{urllib.parse.quote(psid)}"
        headers = {"channel-id": str(channel_id)}
        params = {"pageNo": str(pageNo), "pageSize": str(pageSize)}
        return self._request("GET", path, token=token, headers=headers, params=params)


