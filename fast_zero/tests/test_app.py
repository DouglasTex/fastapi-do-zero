from http import HTTPStatus


def test_read_root_must_return_ok_and_aoba(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Aoba"}


def test_html_end_point_return_ok_and_html_aoba(client):
    response = client.get("/aoba")

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
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
    )


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testuser",
        "email": "test@test.com",
        "id": 1
    }


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "testuser",
                "email": "test@test.com",
                "id": 1
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            'password': 'password',
            "username": "macacomanco",
            "email": "macaco@manco.com",
            "id": 1
        }
    )

    assert response.json() == {
        "username": "macacomanco",
        "email": "macaco@manco.com",
        "id": 1
    }


def test_update_user_error(client):
    response = client.put(
        "/users/9",
        json={
            'password': 'password',
            "username": "macacomanco",
            "email": "macaco@manco.com",
            "id": 1
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_get_user(client):
    response = client.get('/users/1')
    assert response.json() == {
        "username": "macacomanco",
        "email": "macaco@manco.com",
        "id": 1
    }


def test_get_user_error(client):
    response = client.get('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_error(client):
    response = client.delete('/users/9')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'
