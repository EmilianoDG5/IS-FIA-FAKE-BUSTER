def test_segnalazione_post(client, logged_user):
    response = client.post(
        "/segnala/1",
        data={"motivo": "Notizia sospetta"},
        follow_redirects=True
    )

    assert response.status_code == 200
