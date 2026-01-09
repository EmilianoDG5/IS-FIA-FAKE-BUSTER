from app.services.ai_service import is_gibberish

def test_gibberish_true():
    assert is_gibberish("aaaa bbbb cccc dddd eeee ffff") is True

def test_gibberish_false():
    assert is_gibberish(
        "This is a meaningful sentence written in English."
    ) is False
