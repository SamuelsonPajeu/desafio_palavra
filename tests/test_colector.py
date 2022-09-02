from desafio_palavras_app import colector


def test_collector():
    c = colector.Colector("palavra")
    assert isinstance(c.start(), dict) is True
