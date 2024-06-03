import requests
from .exceptions import AuthenticationError, NotFoundError
from typing import Dict

class VYSPClient:
    '''
    Class for interacting with the VYSP.AI API.
    '''
    def __init__(self, tenant_api_key, gate_api_key, installation_type="cloud", installation_url=None):
        self.tenant_api_key = tenant_api_key
        self.gate_api_key = gate_api_key
        self.installation_type = installation_type
        self.base_url = "https://vyspcloud.com/" if installation_type == "cloud" else installation_url

    def _send_request(self, endpoint, method="post", data: Dict = None):
        headers = {
            "Content-Type": "application/json",
            "X-Tenant-Key": self.tenant_api_key,
            "X-Gate-Key": self.gate_api_key,
            "X-Check-Type": data.pop('check_type', 'input') if data else 'output'
        }
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, json=data, headers=headers)

        if response.status_code == 404:
            raise NotFoundError("Resource not found")
        elif response.status_code >= 400:
            raise AuthenticationError("Authentication failed")

        return response.json()

    def check_input(self, client_ref_user_id, prompt, client_ref_internal=False, metadata=None):
        data = {
            "client_ref_user_id": client_ref_user_id,
            "client_ref_internal": client_ref_internal,
            "prompt": prompt,
            "log_metadata": metadata,
            "check_type": "input"
        }
        return self._send_request("gate_check", data=data)

    def check_output(self, client_ref_user_id, prompt, model_output=None, client_ref_internal=False, metadata=None):
        data = {
            "client_ref_user_id": client_ref_user_id,
            "client_ref_internal": client_ref_internal,
            "prompt": prompt,
            "model_output": model_output,
            "log_metadata": metadata,
            "check_type": "output"
        }
        return self._send_request("gate_check", data=data)