def test_creazione_appello(client, logged_user):
    response = client.post(
        "/fact_checker/appelli/create/1",
        data={"motivazione": "Il post è corretto"},
        follow_redirects=True
    )

    assert response.status_code == 200