from app import app

client = app.test_client()


def post(op, a, b):
    return client.post('/' + op, json={'a': a, 'b': b})


def test_add():
    assert post('add', 2, 3).get_json()['result'] == 5


def test_subtract():
    assert post('subtract', 5, 3).get_json()['result'] == 2


def test_multiply():
    assert post('multiply', 4, 6).get_json()['result'] == 24


def test_divide():
    assert post('divide', 10, 4).get_json()['result'] == 2.5


def test_divide_by_zero():
    r = post('divide', 1, 0)
    assert r.status_code == 400


def test_bad_input():
    r = post('add', 'abc', 1)
    assert r.status_code == 400


def test_version():
    assert 'version' in client.get('/version').get_json()


def test_index():
    assert client.get('/').status_code == 200
