import os
from enum import Enum

import backoff
import requests
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

BASE_URL = "https://api.explorium.ai/v1"
EXPLORIUM_API_KEY = os.environ.get("EXPLORIUM_API_KEY")

if not EXPLORIUM_API_KEY:
    raise ValueError(
        "EXPLORIUM_API_KEY environment variable is not set. "
        "Please set it to your Explorium API key."
    )

mcp = FastMCP("Explorium", dependencies=["requests", "pydantic", "dotenv"])


def make_api_request(url, payload, headers=None, timeout=30, max_retries=2, backoff_factor=0.3):
    """
    Makes an API request to the specified endpoint with a JSON payload, using retries on certain failures.
    """
    if headers is None:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api_key": EXPLORIUM_API_KEY,
        }

    full_url = f"{BASE_URL}/{url}"

    # Convert the payload to a serializable format
    serializable_payload = pydantic_model_to_serializable(payload)

    # Define a helper function that will be retried on request exceptions.
    @backoff.on_exception(
        backoff.expo,
        requests.RequestException,
        max_tries=max_retries,
        factor=backoff_factor
    )
    def do_post():
        response = requests.post(full_url, json=serializable_payload, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an error for non-2xx responses
        return response

    try:
        response = do_post()
        return response.json()
    except requests.RequestException as e:
        # Return error information, including the HTTP status code if available.
        return {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
        }


def get_filters_payload(filters) -> dict:
    """Convert filters dict model to request format.

    Converts each non-None filter into a dict with format:
    {"type": "includes", "values": [value1, value2, ...]}
    """
    request_filters = {}

    for field, value in pydantic_model_to_serializable(
            filters, exclude_none=True
    ).items():
        if isinstance(value, dict):
            request_filters[field] = value
        elif isinstance(value, list):
            if len(value) == 0:
                continue
            if isinstance(value[0], Enum):
                request_filters[field] = {
                    "values": enum_list_to_serializable(value),
                }
            else:
                request_filters[field] = {
                    "values": value,
                }
        elif isinstance(value, bool):
            request_filters[field] = {
                "value": value,
            }
        else:
            request_filters[field] = {
                "value": value,
            }

    return request_filters


def enum_list_to_serializable(enum_list: list[Enum]):
    return [str(item.value) for item in enum_list]


def pydantic_model_to_serializable(
        model: BaseModel | list[BaseModel] | dict, exclude_none=False
):
    # Recursively convert all Pydantic models in the object to dicts
    if isinstance(model, BaseModel) and hasattr(model, "model_dump"):
        return model.model_dump(exclude_none=exclude_none)
    elif hasattr(model, "default"):
        return model.default
    elif isinstance(model, list):
        return [
            pydantic_model_to_serializable(item, exclude_none=exclude_none)
            for item in model
        ]
    elif isinstance(model, dict):
        return {
            k: pydantic_model_to_serializable(v, exclude_none=exclude_none)
            for k, v in model.items()
        }
    else:
        return model
