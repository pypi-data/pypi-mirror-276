import pathlib

path = pathlib.Path(__file__).parent


def test():
    with open(path / 'data/test.txt', 'r') as f:
        return f.read()
