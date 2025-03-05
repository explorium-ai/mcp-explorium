from pydantic import BaseModel
from enum import Enum


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
    return [item.value for item in enum_list]


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
