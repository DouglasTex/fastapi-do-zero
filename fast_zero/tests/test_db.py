from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="macacomanco",
        email="email@mail.com",
        password="senhadahora123",
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(select(User).where(User.email == "email@mail.com"))

    assert result.username == "macacomanco"
