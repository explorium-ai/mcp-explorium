from typing import Any, Dict
from unittest.mock import patch

import pytest

from explorium_mcp_server import models
from explorium_mcp_server.tools.prospects import (
    match_prospects,
    fetch_prospects,
    fetch_prospects_events,
    enrich_prospects_contacts_information,
    enrich_prospects_linkedin_posts,
    enrich_prospects_profiles,
)

PROS_MOD_PATH = "explorium_mcp_server.tools.prospects"


def _response(payload: Dict[str, Any]):
    return {"echo": payload}


def test_match_prospects_calls_api_correctly():
    good_input = [
        models.prospects.ProspectMatchInput(email="a@acme.com")  # type: ignore[arg-type]
    ]
    expected_payload = {"prospects_to_match": good_input}
    with patch(f"{PROS_MOD_PATH}.make_api_request", return_value=_response(expected_payload)) as m:
        result = match_prospects(good_input)
    m.assert_called_once_with("prospects/match", expected_payload)
    assert result == _response(expected_payload)


@pytest.mark.parametrize("size,page_size,page", [(1000, 5, 1), (150, 10, 3)])
def test_fetch_prospects_builds_payload(size: int, page_size: int, page: int):
    dummy_filters = models.prospects.FetchProspectsFilters()
    with patch(f"{PROS_MOD_PATH}.get_filters_payload", return_value={"dummy": True}) as gf, patch(
            f"{PROS_MOD_PATH}.make_api_request",
            return_value=_response({"size": size}),
    ) as m:
        result = fetch_prospects(dummy_filters, size=size, page_size=page_size, page=page)
    gf.assert_called_once_with(dummy_filters)
    expected_payload = {
        "mode": "full",
        "size": size,
        "page_size": page_size,
        "page": page,
        "filters": {"dummy": True},
    }
    m.assert_called_once_with("prospects", expected_payload)
    assert result == _response({"size": size})


def test_fetch_prospects_events_payload():
    ids_ = ["p1", "p2"]
    events = [models.prospects.ProspectEventType.JOB_TITLE_CHANGE]  # type: ignore[arg-type]
    with patch(f"{PROS_MOD_PATH}.enum_list_to_serializable", return_value=["role_change"]) as enum_conv, patch(
            f"{PROS_MOD_PATH}.make_api_request",
            return_value=_response({"ok": True}),
    ) as m:
        result = fetch_prospects_events(
            prospect_ids=ids_,
            event_types=events,
            timestamp_from="2024-01-01T00:00:00Z",
        )
    enum_conv.assert_called_once_with(events)
    expected_payload = {
        "prospect_ids": ids_,
        "event_types": ["role_change"],
        "timestamp_from": "2024-01-01T00:00:00Z",
    }
    m.assert_called_once_with("prospects/events", expected_payload, timeout=120)
    assert result == _response({"ok": True})


def test_enrich_contacts_information_pass_through():
    ids_ = ["p1"]
    with patch(f"{PROS_MOD_PATH}.make_api_request", return_value=_response({"ids": ids_})) as m:
        result = enrich_prospects_contacts_information(ids_)
    m.assert_called_once_with("prospects/contacts_information/bulk_enrich", {"prospect_ids": ids_})
    assert result == _response({"ids": ids_})


def test_enrich_linkedin_posts_pass_through():
    ids_ = ["p1", "p2"]
    with patch(f"{PROS_MOD_PATH}.make_api_request", return_value=_response({"ids": ids_})) as m:
        result = enrich_prospects_linkedin_posts(ids_)
    m.assert_called_once_with("prospects/linkedin_posts/bulk_enrich", {"prospect_ids": ids_})
    assert result == _response({"ids": ids_})


def test_enrich_profiles_pass_through():
    ids_ = ["p1", "p2", "p3"]
    with patch(f"{PROS_MOD_PATH}.make_api_request", return_value=_response({"ids": ids_})) as m:
        result = enrich_prospects_profiles(ids_)
    m.assert_called_once_with("prospects/profiles/bulk_enrich", {"prospect_ids": ids_})
    assert result == _response({"ids": ids_})
