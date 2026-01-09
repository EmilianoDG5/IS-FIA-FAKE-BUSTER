def test_creazione_appello(client, logged_user):
    response = client.post(
        "/appelli/1",
        data={"motivazione": "Il post è corretto"},
        follow_redirects=True
    )

    assert response.status_code == 200