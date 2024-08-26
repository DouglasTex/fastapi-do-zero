from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
        "id": 1,
    }


def test_create_user_error_username_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "macacomanco",
            "email": "macaco@manco.com",
            "password": "password",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


def test_create_user_error_email_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "macacomanco2",
            "email": "macaco@manco.com",
            "password": "password",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already exists'


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    # como user vem como um tipo do sqlalchemy,
    # precisamos transformar isso de volta em um modelo que usamos no back,
    # que no caso é o UserPublic
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "password": "password",
            "username": "macacomanco",
            "email": "macaco@manco.com",
            "id": 1,
        },
    )

    assert response.json() == {
        "username": "macacomanco",
        "email": "macaco@manco.com",
        "id": 1,
    }


def test_update_user_error(client):
    response = client.put(
        "/users/9",
        json={
            "password": "password",
            "username": "macacomanco",
            "email": "macaco@manco.com",
            "id": 1,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_get_user(client, user):
    response = client.get("/users/1")
    assert response.json() == {
        "username": "macacomanco",
        "email": "macaco@manco.com",
        "id": 1,
    }


def test_get_user_error(client):
    response = client.get("/users/0")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_delete_user(client, user):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted"}


def test_delete_user_error(client):
    response = client.delete("/users/9")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"
