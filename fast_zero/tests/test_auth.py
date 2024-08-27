from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_get_token_bad_request(client):
    response = client.post(
        "/auth/token",
        data={"username": "not_a_mail@mail.com", "password": "not_a_pass"}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
