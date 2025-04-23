from enum import Enum
from typing import Any, Dict, List
from unittest.mock import patch

from pydantic import BaseModel

from explorium_mcp_server.tools.shared import enum_list_to_serializable, pydantic_model_to_serializable, \
    make_api_request, get_filters_payload


class ExampleEnum(Enum):
    FOO = "foo"
    BAR = "bar"


class ExampleModel(BaseModel):
    name: str
    age: int | None = None


def _make_response(status_code: int, json_data: Dict[str, Any] | List[Any]):
    """Create a real requests.Response object with prepared JSON payload."""
    import json
    import requests

    response = requests.Response()
    response.status_code = status_code
    response._content = json.dumps(json_data).encode()
    return response


def test_enum_list_to_serializable():
    enum_values = [ExampleEnum.FOO, ExampleEnum.BAR]
    assert enum_list_to_serializable(enum_values) == ["foo", "bar"]


def test_pydantic_model_to_serializable_base():
    model = ExampleModel(name="Alice", age=30)
    assert pydantic_model_to_serializable(model) == {"name": "Alice", "age": 30}


def test_pydantic_model_to_serializable_exclude_none():
    model = ExampleModel(name="Bob")
    assert pydantic_model_to_serializable(model, exclude_none=True) == {"name": "Bob"}


def test_pydantic_model_to_serializable_nested():
    models = [ExampleModel(name="A", age=1), ExampleModel(name="B", age=2)]
    expected = [{"name": "A", "age": 1}, {"name": "B", "age": 2}]
    assert pydantic_model_to_serializable(models) == expected


def test_get_filters_payload_various_types():
    filters = {
        "enum_list": [ExampleEnum.FOO, ExampleEnum.BAR],
        "str_list": ["x", "y"],
        "boolean": True,
        "simple_value": "abc",
    }
    payload = get_filters_payload(filters)
    assert payload == {
        "enum_list": {"values": ["foo", "bar"]},
        "str_list": {"values": ["x", "y"]},
        "boolean": {"value": True},
        "simple_value": {"value": "abc"},
    }


def test_make_api_request_success():
    """Verify that a successful 200 response returns parsed JSON."""

    def fake_request(*args, **kwargs):
        return _make_response(200, {"ok": True})

    with patch("requests.request", fake_request):
        result = make_api_request("dummy/endpoint")
    assert result == {"ok": True}


def test_make_api_request_error():
    """Verify that on HTTP error the function returns error dict instead of raising."""
    import requests

    class MyError(requests.HTTPError):
        pass

    def fake_request(*args, **kwargs):
        response = _make_response(404, {"detail": "Not found"})
        http_err = MyError("404 Client Error: Not Found for url", response=response)
        raise http_err

    with patch("requests.request", fake_request):
        result = make_api_request("dummy/endpoint")
    assert result["status_code"] == 404
    assert "error" in result
