from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testuser',
        'email': 'test@test.com',
        'id': 1,
    }


def test_create_user_error_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


def test_create_user_error_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'new_username',
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already exists'


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    # como user vem como um tipo do sqlalchemy,
    # precisamos transformar isso de volta em um modelo que usamos no back,
    # que no caso é o UserPublic
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'macacomanco',
            'email': 'macaco@manco.com',
            'password': 'password',
        },
    )

    assert response.json() == {
        'username': 'macacomanco',
        'email': 'macaco@manco.com',
        'id': 1,
    }


def test_update_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'macacomanco',
            'email': 'macaco@manco.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_update_user_error(client):
    response = client.put(
        '/users/9',
        json={
            'password': 'password',
            'username': 'macacomanco',
            'email': 'macaco@manco.com',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'


def test_update_user_unauthorized(client, user):
    response = client.put(
        '/users/2',
        json={
            'password': 'password',
            'username': 'macacomanco',
            'email': 'macaco@manco.com',
            'id': 2,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_get_user_error(client):
    response = client.get('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_error(client):
    response = client.delete('/users/9')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
