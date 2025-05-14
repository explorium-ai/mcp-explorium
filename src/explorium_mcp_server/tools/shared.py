import logging
import os
from enum import Enum
from typing import Optional, Any, Dict

import backoff
import requests
from fastmcp import FastMCP
from pydantic import BaseModel

from explorium_mcp_server.storage import (
    generate_session_id,
    store_session_data,
    load_session_data,
    list_session_keys,
    delete_session_data
)

logger = logging.getLogger(__name__)

BASE_URL = "https://api.explorium.ai/v1"
EXPLORIUM_API_KEY = os.environ.get("EXPLORIUM_API_KEY")

if not EXPLORIUM_API_KEY:
    logger.warning("EXPLORIUM_API_KEY environment variable is not set.")
    raise ValueError(
        "EXPLORIUM_API_KEY environment variable is not set. "
        "Please set it to your Explorium API key."
    )

mcp = FastMCP("Explorium", dependencies=["requests", "pydantic", "dotenv", "duckdb"])


def make_api_request(
        url: str,
        payload=None,
        headers=None,
        timeout=30,
        max_retries=2,
        backoff_factor=0.3,
        method: str = "POST",
        params: Optional[dict] = None,
        session_id: Optional[str] = None,
        session_key: Optional[str] = None
):
    """
    Makes an API request to the specified endpoint with retries on certain failures.

    :param url: Relative path to the API endpoint.
    :param payload: Request payload (used in POST/PUT/PATCH).
    :param headers: Optional request headers.
    :param timeout: Timeout for the request in seconds.
    :param max_retries: Maximum number of retry attempts.
    :param backoff_factor: Exponential backoff factor.
    :param method: HTTP method to use ('GET', 'POST', 'PUT', 'DELETE', etc.).
    :param params: Query parameters for GET or other requests.
    :param session_id: Optional session ID for storing results
    :param session_key: Optional key to store results under in the session
    :return: Parsed JSON response or error info.
    """
    if headers is None:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api_key": EXPLORIUM_API_KEY,
        }

    full_url = f"{BASE_URL}/{url}"

    if payload is not None:
        payload = pydantic_model_to_serializable(payload)

    @backoff.on_exception(
        backoff.expo,
        requests.RequestException,
        max_tries=max_retries,
        factor=backoff_factor
    )
    def do_request():
        logger.info(f"Sending {method.upper()} request to {full_url}, payload: {payload}, params: {params}")
        response = requests.request(
            method=method.upper(),
            url=full_url,
            json=payload if method.upper() in {"POST", "PUT", "PATCH"} else None,
            params=params,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        return response

    try:
        response = do_request()
        response.raise_for_status()  # Raise an error for non-2xx responses
        result = response.json()
        
        # Store result in session storage if session_id and session_key are provided
        if session_id and session_key:
            store_session_data(session_id, session_key, result)
            
        return result
    except requests.RequestException as e:
        logger.warning(f"Failed to send {method.upper()} request to {full_url}: {e}")
        return {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
        }
    except Exception as e:
        logger.error(f"Unexpected error during request: {e}")
        return {
            "error": str(e),
            "status_code": None,
        }


def get_filters_payload(filters) -> dict:
    """Convert filters dict model to request format.

    Converts each non-None filter into a dict with format:
    {"type": "includes", "values": [value1, value2, ...]}
    """
    try:
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
    except Exception as e:
        logger.error(f"Error in get_filters_payload: {e}")
        raise ValueError("Failed to convert filters to payload") from e


def enum_list_to_serializable(enum_list: list[Enum]):
    return [str(item.value) for item in enum_list]


def pydantic_model_to_serializable(
        model: BaseModel | list[BaseModel] | dict, exclude_none=False
):
    # Recursively convert all Pydantic models in the object to dicts
    try:
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
    except Exception as e:
        logger.error(f"Error in pydantic_model_to_serializable: {e}")
        raise ValueError("Failed to convert Pydantic model to serializable format") from e


def create_session() -> str:
    """Create a new session and return its ID."""
    return generate_session_id()


def get_session_data(session_id: str, key: str) -> Any:
    """Get data from a session."""
    return load_session_data(session_id, key)


def save_session_data(session_id: str, key: str, data: Any) -> None:
    """Save data to a session."""
    store_session_data(session_id, key, data)


def get_session_keys(session_id: str) -> list:
    """Get all keys in a session."""
    return list_session_keys(session_id)


def clear_session(session_id: str, key: Optional[str] = None) -> None:
    """Clear a session or a specific key in a session."""
    delete_session_data(session_id, key)
