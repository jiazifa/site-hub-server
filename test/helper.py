import os

import pytest
from typing import Any, Union
from flask.testing import FlaskClient
from flask import Flask
from app import create_app

@pytest.fixture(scope="module")
def app() -> Flask:
    os.environ.setdefault("TESTING", "True")
    app = create_app()
    return app


@pytest.fixture(scope="module")
def client(app: Flask) -> FlaskClient:
    return app.test_client()
