from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, Any
import os
from pydantic import BaseModel
from enum import Enum

# Get API key from environment variables
EXPLORIUM_API_KEY = os.environ.get("EXPLORIUM_API_KEY")
BASE_URL = "https://api.explorium.ai/v1"

if not EXPLORIUM_API_KEY:
    raise ValueError("EXPLORIUM_API_KEY is not set")

mcp = FastMCP("Explorium", dependencies=["requests", "pydantic", "dotenv"])


def make_api_request(url, payload, headers=None):
    """Helper function to make API requests with consistent error handling"""
    if headers is None:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api_key": EXPLORIUM_API_KEY,
        }

    try:
        serializable_payload = pydantic_model_to_serializable(payload)
        response = requests.post(
            f"{BASE_URL}/{url}", json=serializable_payload, headers=headers
        )
        # response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
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

    for field, value in filters.model_dump(exclude_none=True).items():
        if isinstance(value, list):
            if isinstance(value[0], Enum):
                request_filters[field] = {
                    "type": "includes",
                    "values": enum_list_to_serializable(value),
                }
            else:
                request_filters[field] = {
                    "type": "includes",
                    "values": value,
                }
        elif isinstance(value, bool):
            request_filters[field] = {
                "type": "exists",
                "value": value,
            }
        else:
            request_filters[field] = {
                "type": "includes",
                "value": value,
            }

    return request_filters


def enum_list_to_serializable(enum_list: list[Enum]):
    return [str(item.value) for item in enum_list]


def pydantic_model_to_serializable(model: BaseModel | list[BaseModel] | dict):
    # Recursively convert all Pydantic models in the object to dicts
    if isinstance(model, BaseModel):
        return model.model_dump()
    elif isinstance(model, list):
        return [pydantic_model_to_serializable(item) for item in model]
    elif isinstance(model, dict):
        return {k: pydantic_model_to_serializable(v) for k, v in model.items()}
    else:
        return model
