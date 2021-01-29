from typing import Dict, Any
import random
from common import get_random_num
from flask.testing import FlaskClient
from .helper import *


class TestWebsite:
    def setup_method(self):

        self._email = DEFAULT_LOGIN_PARAMS.get("email", "")
        self._password = DEFAULT_LOGIN_PARAMS.get("password", "")

    #测试创建分类
    def test_create_category(self, client):
        token = get_token(client, DEFAULT_LOGIN_PARAMS)
        name = random.choice(["测试1", "测试2", "测试3", "测试4"])

        rv = client.post("/api/site/category",
                         json={"name": name},
                         headers={"token": token})
        if rv.status_code == 200:
            body = rv.json["data"]
            assert body.get("id") != None
        else:
            assert rv.status_code == 201

    # 测试查询分类列表
    def test_query_categories(self, client):
        token = get_token(client, DEFAULT_LOGIN_PARAMS)

        rv = client.get("/api/site/categories", headers={"token": token})
        assert rv.status_code == 200
        body = rv.json["data"]
        assert body != None

    def test_create_site(self, client: FlaskClient):
        token = get_token(client, DEFAULT_LOGIN_PARAMS)

        rv = client.get("/api/site/categories", headers={"token": token})
        assert rv.status_code == 200
        body = rv.json["data"]
        cid: int = len(body) > 0

        rv = client.post("/api/site/create",
                         json={
                             "name": "{}".format(get_random_num(4)),
                             "url": "http://www.baidu.com/{}".format(get_random_num(6)),
                             "category_id": cid,
                             "token": token
                         })
        if rv.status_code == 200:
            body = rv.json["data"]
            assert body.get("id") != None
        else:
            assert rv.status_code == 201
