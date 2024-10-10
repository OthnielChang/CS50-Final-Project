import pytest
from project import counter, word_processor, predict, blacklist, rooter_for_tokens, rooter_for_words

def test_counter():
    assert counter(["miracle","hello"]) == [1,1]
    assert counter(["miracle","million","good","hello","normal"]) == [3,2]

def test_word_processor():
    assert word_processor("I went to a place that had millions of dollars") == ["I", "go", "place", "million", "dollar"]
    assert word_processor("Money is here, there, everywhere!") == ["Money", "everywhere"]

def test_predict():
    assert predict(8, 2) == "Your message is likely not a scam, with 80% certainty"
    assert predict(2, 2) == "Your message could be a scam"
    assert predict(2, 8) == "Your message is likely a scam, with 80% certainty"

def test_blacklist():
    assert blacklist("scam@gmail.com") == True
    assert blacklist("scam@@gmail.com") == False
    assert blacklist("scam@gm..ail.co!m") == False

def test_rooter_for_tokens():
    assert rooter_for_tokens("promised") == ["p", "r", "o", "m", "i", "s", "e", "d"]
    assert rooter_for_tokens("millions") == ["m", "i", "l", "l", "i", "o", "n", "s"]

def test_rooter_for_words():
    assert rooter_for_words("promised") == "promise"
    assert rooter_for_words("millions") == "million"