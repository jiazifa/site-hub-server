import os
from flask.testing import FlaskClient
from .helper import *


class TestOneWord:
    def test_add_word(self, client: FlaskClient):

        rv = client.post("/api/oneword/",
                         json={"content": "测试添加的数据"})
        assert rv.status_code == 200

    def test_get_one_word(self, client: FlaskClient):

        rv = client.get("api/oneword/")
        assert rv.status_code == 200
        body: str = rv.json["data"]
        assert body != None

    def test_get_word_by_id(self, client: FlaskClient):

        rv = client.get("api/oneword/1")
        assert rv.status_code == 200
        body: str = rv.json["data"]
        assert body != None