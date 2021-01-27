import os

import pytest
from typing import Any, Union
from flask.testing import FlaskClient
from flask import Flask
from app import create_app

DEFAULT_LOGIN_PARAMS = {
    "email": "123456789@qq.com",
    "password": "e10adc3949ba59abbe56e057f20f883e"
}


def get_token(client, login_params) -> str:
    rv = client.post("/api/user/login", json=login_params)
    return str(rv.json["data"]["token"])


@pytest.fixture(scope="module")
def app() -> Flask:
    os.environ.setdefault("TESTING", "True")
    app = create_app()
    return app


@pytest.fixture(scope="module")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="module")
def token(client) -> str:
    rv = client.post("/api/user/login", json=DEFAULT_LOGIN_PARAMS)
    assert rv.status_code == 200
    return str(rv.json["data"]["token"])


@pytest.fixture(scope="module")
def user_id(client) -> str:
    rv = client.post("/api/user/login", json=DEFAULT_LOGIN_PARAMS)
    assert rv.status_code == 200
    return str(rv.json["data"]["user_id"])