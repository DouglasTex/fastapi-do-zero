from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_must_return_ok_and_aoba():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Aoba'}


def test_html_end_point_return_ok_and_html_aoba():
    client = TestClient(app)

    response = client.get('/aoba')

    assert response.status_code == HTTPStatus.OK
    assert response.text == """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Página teste</title>
        </head>
        <body>
            <p>Aoba</p>
        </body>
        </html>
        """  # noqa: E501
