import pytest

from app.services.api_football import get_from_api


def test_get_from_api_returns_response(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "errors": [],
                "response": [
                    {
                        "id": 135,
                        "name": "Serie A"
                    }
                ]
            }

    def fake_requests_get(
        url,
        headers=None,
        params=None,
        timeout=None
    ):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.api_football.requests.get",
        fake_requests_get
    )

    result = get_from_api(
        endpoint="leagues",
        params={
            "id": 135,
            "season": 2024
        }
    )

    assert len(result) == 1
    assert result[0]["id"] == 135
    assert result[0]["name"] == "Serie A"


def test_get_from_api_raises_api_error(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "errors": {
                    "plan": "Free plans do not have access to this season."
                },
                "response": []
            }

    def fake_requests_get(
        url,
        headers=None,
        params=None,
        timeout=None
    ):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.api_football.requests.get",
        fake_requests_get
    )

    with pytest.raises(ValueError) as error:
        get_from_api(
            endpoint="leagues",
            params={
                "id": 135,
                "season": 2025
            }
        )

    assert "API-Football error" in str(error.value)


def test_get_from_api_returns_empty_list_when_response_missing(
    monkeypatch
):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "errors": []
            }

    def fake_requests_get(
        url,
        headers=None,
        params=None,
        timeout=None
    ):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.api_football.requests.get",
        fake_requests_get
    )

    result = get_from_api(
        endpoint="leagues"
    )

    assert result == []