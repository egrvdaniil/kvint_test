def test_get_industry_values(api_client):
    response = api_client.get(
        "/",
        params={
            'period_start': 2017,
            'period_end': 2019,
            'industry_number': '21'
        },
    )
    assert response.ok
