from pydantic import BaseModel


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
                    "values": [item.value for item in value],
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


def pydantic_model_to_serializable(model: BaseModel):
    # Recursively convert all Pydantic models in the object to dicts
    if isinstance(model, BaseModel):
        return model.model_dump()
    elif isinstance(model, list):
        return [pydantic_model_to_serializable(item) for item in model]
    elif isinstance(model, dict):
        return {k: pydantic_model_to_serializable(v) for k, v in model.items()}
    else:
        return model
