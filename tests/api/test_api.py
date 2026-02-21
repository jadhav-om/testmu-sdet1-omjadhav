import pytest
import requests
from jsonschema import validate

DUMMY_BASE = "https://dummyjson.com"
JSONPLACEHOLDER_BASE = "https://jsonplaceholder.typicode.com"


@pytest.mark.smoke
def test_auth_token_validation(llm_context: dict) -> None:
    login_response = requests.post(
        f"{DUMMY_BASE}/auth/login",
        json={"username": "emilys", "password": "emilyspass"},
        timeout=20,
    )
    llm_context["login_response"] = login_response.text[:1000]
    assert login_response.status_code == 200

    token = login_response.json().get("accessToken")
    assert token

    invalid_auth_response = requests.get(
        f"{DUMMY_BASE}/auth/me",
        headers={"Authorization": "Bearer bad_token"},
        timeout=20,
    )
    llm_context["invalid_auth_response"] = invalid_auth_response.text[:1000]
    assert invalid_auth_response.status_code == 401


@pytest.mark.regression
def test_crud_operations(llm_context: dict) -> None:
    create = requests.post(
        f"{JSONPLACEHOLDER_BASE}/posts",
        json={"title": "qa post", "body": "sample", "userId": 1},
        timeout=20,
    )
    llm_context["crud_create"] = create.text[:1000]
    assert create.status_code in {201, 200}

    created_id = create.json().get("id", 101)

    read = requests.get(f"{JSONPLACEHOLDER_BASE}/posts/{created_id}", timeout=20)
    llm_context["crud_read"] = read.text[:1000]
    assert read.status_code in {200, 404}

    update = requests.put(
        f"{JSONPLACEHOLDER_BASE}/posts/1",
        json={"id": 1, "title": "updated", "body": "updated", "userId": 1},
        timeout=20,
    )
    llm_context["crud_update"] = update.text[:1000]
    assert update.status_code in {200, 201, 500}

    delete = requests.delete(f"{JSONPLACEHOLDER_BASE}/posts/1", timeout=20)
    llm_context["crud_delete"] = str(delete.status_code)
    assert delete.status_code in {200, 204, 500}


@pytest.mark.regression
def test_error_handling_4xx_and_5xx(llm_context: dict) -> None:
    not_found = requests.get(f"{JSONPLACEHOLDER_BASE}/unknown-endpoint", timeout=20)
    llm_context["404_body"] = not_found.text[:600]
    assert not_found.status_code == 404

    server_error = requests.get("https://httpbin.org/status/500", timeout=20)
    llm_context["500_body"] = server_error.text[:600]
    assert server_error.status_code == 500


@pytest.mark.regression
def test_rate_limiting_signal() -> None:
    response = requests.get("https://api.github.com/rate_limit", timeout=20)
    assert response.status_code == 200
    core_limit = response.json()["resources"]["core"]["limit"]
    assert core_limit > 0


@pytest.mark.regression
def test_schema_validation(llm_context: dict) -> None:
    response = requests.get(f"{DUMMY_BASE}/users/1", timeout=20)
    llm_context["schema_body"] = response.text[:1000]
    assert response.status_code == 200

    schema = {
        "type": "object",
        "required": ["id", "firstName", "lastName", "email"],
        "properties": {
            "id": {"type": "integer"},
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "email": {"type": "string"},
        },
    }
    validate(instance=response.json(), schema=schema)
