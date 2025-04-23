from typing import Any, Dict, List, Tuple, Callable
from unittest.mock import patch

import pytest

from explorium_mcp_server import models
from explorium_mcp_server.tools.businesses import (
    match_businesses,
    fetch_businesses,
    autocomplete,
    fetch_businesses_events,
    fetch_businesses_statistics,
    enrich_businesses_firmographics,
    enrich_businesses_technographics,
    enrich_businesses_company_ratings,
    enrich_businesses_financial_metrics,
    enrich_businesses_funding_and_acquisitions,
    enrich_businesses_challenges,
    enrich_businesses_competitive_landscape,
    enrich_businesses_strategic_insights,
    enrich_businesses_workforce_trends,
    enrich_businesses_linkedin_posts,
    enrich_businesses_website_changes,
    enrich_businesses_website_keywords,
)

BUS_MOD_PATH = "explorium_mcp_server.tools.businesses"


def _response(payload: Dict[str, Any]):
    return {"echo": payload}


# ---- core tools -----------------------------------------------------------

def test_match_businesses():
    items = [models.businesses.MatchBusinessInput(name="Acme", domain="acme.com")]
    expected = {"businesses_to_match": items}
    with patch(f"{BUS_MOD_PATH}.make_api_request", return_value=_response(expected)) as m:
        out = match_businesses(items)
    m.assert_called_once_with("businesses/match", expected)
    assert out == _response(expected)


@pytest.mark.parametrize("size,page_size,page", [(1000, 5, 1), (200, 10, 2)])
def test_fetch_businesses(size, page_size, page):
    filters = models.businesses.FetchBusinessesFilters()
    with patch(f"{BUS_MOD_PATH}.get_filters_payload", return_value={"f": 1}) as gf, patch(
            f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"n": size})
    ) as m:
        out = fetch_businesses(filters, size=size, page_size=page_size, page=page)
    gf.assert_called_once_with(filters)
    m.assert_called_once_with(
        "businesses",
        {
            "mode": "full",
            "size": size,
            "page_size": min(page_size, size),
            "page": page,
            "filters": {"f": 1},
            "request_context": {},
        },
    )
    assert out == _response({"n": size})


def test_autocomplete():
    with patch(f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"ok": True})) as m:
        out = autocomplete("country", "isr")  # type: ignore[arg-type]
    m.assert_called_once_with(
        "businesses/autocomplete",
        method="GET",
        params={"field": "country", "query": "isr"},
    )
    assert out == _response({"ok": True})


def test_fetch_businesses_events():
    ids_ = ["a"]
    events = [models.businesses.BusinessEventType.NEW_PRODUCT]
    with patch(f"{BUS_MOD_PATH}.enum_list_to_serializable", return_value=["new_product"]) as enum_conv, patch(
            f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"e": True})
    ) as m:
        out = fetch_businesses_events(ids_, events, timestamp_from="2024-01-01T00:00:00Z")
    enum_conv.assert_called_once_with(events)
    m.assert_called_once_with(
        "businesses/events",
        {
            "business_ids": ids_,
            "event_types": ["new_product"],
            "timestamp_from": "2024-01-01T00:00:00Z",
        },
        timeout=120,
    )
    assert out == _response({"e": True})


def test_fetch_businesses_statistics():
    filters = models.businesses.FetchBusinessesFilters()
    with patch(f"{BUS_MOD_PATH}.get_filters_payload", return_value={"x": 1}) as gf, patch(
            f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"stat": True})
    ) as m:
        out = fetch_businesses_statistics(filters)
    gf.assert_called_once_with(filters)
    m.assert_called_once_with("businesses/stats", {"filters": {"x": 1}})
    assert out == _response({"stat": True})


# ---- enrichment sets ------------------------------------------------------

_ENRICH_SIMPLE: List[Tuple[Callable[..., Dict[str, Any]], str]] = [
    (enrich_businesses_firmographics, "businesses/firmographics/bulk_enrich"),
    (enrich_businesses_technographics, "businesses/technographics/bulk_enrich"),
    (enrich_businesses_company_ratings, "businesses/company_ratings_by_employees/bulk_enrich"),
    (enrich_businesses_funding_and_acquisitions, "businesses/funding_and_acquisition/bulk_enrich"),
    (enrich_businesses_challenges, "businesses/pc_business_challenges_10k/bulk_enrich"),
    (enrich_businesses_competitive_landscape, "businesses/pc_competitive_landscape_10k/bulk_enrich"),
    (enrich_businesses_strategic_insights, "businesses/pc_strategy_10k/bulk_enrich"),
    (enrich_businesses_workforce_trends, "businesses/workforce_trends/bulk_enrich"),
    (enrich_businesses_linkedin_posts, "businesses/linkedin_posts/bulk_enrich"),
]


@pytest.mark.parametrize("func,endpoint", _ENRICH_SIMPLE)
def test_enrich_simple(func, endpoint):
    ids_ = ["b1"]
    with patch(f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"ids": ids_})) as m:
        out = func(ids_)
    m.assert_called_once_with(endpoint, {"business_ids": ids_})
    assert out == _response({"ids": ids_})


def test_enrich_financial_metrics_with_date():
    ids_ = ["b1"]
    with patch(f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"ids": ids_})) as m:
        out = enrich_businesses_financial_metrics(ids_, date="2024-01-01")
    m.assert_called_once_with(
        "businesses/financial_indicators/bulk_enrich",
        {"business_ids": ids_, "parameters": {"date": "2024-01-01"}},
    )
    assert out == _response({"ids": ids_})


def test_enrich_website_changes_keywords():
    ids_ = ["b1"]
    kw = ["growth"]
    with patch(f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"ids": ids_})) as m:
        out = enrich_businesses_website_changes(ids_, keywords=kw)
    m.assert_called_once_with(
        "businesses/website_changes/bulk_enrich",
        {"business_ids": ids_, "parameters": {"keywords": kw}},
    )
    assert out == _response({"ids": ids_})


def test_enrich_website_keywords_keywords():
    ids_ = ["b1"]
    kw = ["seo"]
    with patch(f"{BUS_MOD_PATH}.make_api_request", return_value=_response({"ids": ids_})) as m:
        out = enrich_businesses_website_keywords(ids_, keywords=kw)
    m.assert_called_once_with(
        "businesses/company_website_keywords/bulk_enrich",
        {"business_ids": ids_, "parameters": {"keywords": kw}},
    )
    assert out == _response({"ids": ids_})
