from app.services.ai_service import AIService

def test_testo_troppobreve():
    ai = AIService()
    score,  = ai.analyze_text("ciao")
    assert score == -1.0

def test_testorandom():
    ai = AIService()
    score,  = ai.analyze_text("asdf qwerty zxcv asdf qwerty")
    assert score == -1.0

def test_testovalido():
    ai = AIService()
    score,  = ai.analyze_text(
        "This is a long realistic news article with enough content."
    )
    assert isinstance(score, float)