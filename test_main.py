from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_cities():
    """Return the cities with historical weather data for Spain."""
    response = client.get("/countries/Spain")
    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_cities_excludes_cities_outside_country():
    """Only Seville belongs to Spain; cities of other countries are absent."""
    cities = client.get("/countries/Spain").json()
    assert "Seville" in cities
    assert "Madrid" not in cities
    assert "Lisbon" not in cities


def test_cities_only_allows_get():
    """The route only accepts GET requests."""
    response = client.post("/countries/Spain")
    assert response.status_code == 405