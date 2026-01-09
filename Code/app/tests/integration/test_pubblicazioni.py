from unittest.mock import patch

def test_post_bloccato_da_ia(client, logged_user):
    with patch("app.controllers.gestione_pubblicazioni.ai_service") as mock_ai:
        mock_ai.analyze_text.return_value = (0.9, "{}")

        response = client.post(
            "/posts",
            data={
                "titolo": "Fake News",
                "testo": "This is clearly fake content"
            },
            follow_redirects=True
        )

        assert response.status_code == 200

def test_post_pubblicato(client, logged_user):
    with patch("app.controllers.gestione_pubblicazioni.ai_service") as mock_ai:
        mock_ai.analyze_text.return_value = (0.1, "{}")

        response = client.post(
            "/posts",
            data={
                "titolo": "Real News",
                "testo": "This is a realistic and factual article"
            },
            follow_redirects=True
        )

        assert response.status_code == 200