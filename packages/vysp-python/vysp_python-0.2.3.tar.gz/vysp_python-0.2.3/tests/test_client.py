import pytest
from vysp import VYSPClient
from requests_mock import mocker
from vysp import NotFoundError, AuthenticationError

@pytest.fixture
def client():
    return VYSPClient(tenant_api_key="JC48VislL28mgev3CSD9kw", gate_api_key="-7eBRsIqMQDyErwzm1oamQ", installation_type="local", installation_url="http://localhost:8000/")

def test_check_input_success(requests_mock, client):
    requests_mock.post("http://localhost:8000/gate_check", json={"success": True}, status_code=200)
    response = client.check_input("user1", "test input")
    assert response == {"success": True}

def test_check_input_not_found(requests_mock, client):
    requests_mock.post("http://localhost:8000/gate_check", json={"detail": "Not found"}, status_code=404)
    with pytest.raises(NotFoundError):
        client.check_input("user1", "test input")

def test_check_output_success(requests_mock, client):
    requests_mock.post("http://localhost:8000/gate_check", json={"success": True}, status_code=200)
    response = client.check_output("user1", "test output")
    assert response == {"success": True}

def test_check_output_authentication_error(requests_mock, client):
    requests_mock.post("http://localhost:8000/gate_check", json={"detail": "Unauthorized"}, status_code=401)
    with pytest.raises(AuthenticationError):
        client.check_output("user1", "test output")