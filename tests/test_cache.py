import pytest
from desafio_palavras_app import colector


def test_cache():
    c = colector.CachedWords()
    c.enabled = True

    # Test Methods
    assert c.words == {}
    assert c.add("teste1", {"searches": 10}) is None
    assert c.add("teste2", {"searches": 20}) is None
    assert c.add("teste3", {"searches": 30}) is None
    assert isinstance(c.get_less_searched(), str) is True
    assert c.remove("teste1") is None
    assert c.get("teste2") == {"searches": 20}
    assert isinstance(c.count_total(), int) is True
    assert c.__contains__("teste2") is True
    assert c.__contains__("teste1") is False


def test_bad_format():
    c = colector.CachedWords()
    c.enabled = True

    with pytest.raises(colector.FormatNotSupported):
        c.add("teste", "teste")
        c.add(10, {"teste": "teste"})
        c.remove(10)
        c.__contains__(10)
