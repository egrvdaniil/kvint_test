def test_get_industry_values(api_client):
    response = api_client.get(
        "/",
        params={},
    )
    assert response.ok
