from typing import Dict, Any
import random
from flask.testing import FlaskClient
from .helper import *


class TestUser:
    def setup_method(self):

        self._email = DEFAULT_LOGIN_PARAMS.get("email", "")
        self._password = DEFAULT_LOGIN_PARAMS.get("password", "")

    def test_register(self, client: FlaskClient):
        params: Dict[str, str] = {
            "email": self._email,
            "password": self._password,
        }
        rv = client.post("/api/user/register", json=params)
        print(rv.json)
        if rv.status_code == 400 and rv.json["msg"] != None:
            return
        if rv.status_code == 200:
            body: dict = rv.json["data"]
            assert body != None
            assert body["id"] != None
        else:
            assert rv.status_code == 201
        

    # 测试重复注册接口
    def test_register_on_error(self, client):
        password: str = self._password
        rv = client.post("/api/user/register",
                         json={
                             "email": self._email,
                             "password": self._password,
                         })
        rv = client.post("/api/user/register",
                         json={
                             "email": self._email,
                             "password": self._password,
                         })

        assert rv.status_code != 200

    # 测试登录 [账号密码登录]
    def test_login(self, client):
        password = self._password
        rv = client.post("/api/user/login",
                         json={
                             "email": self._email,
                             "password": self._password,
                         })
        assert rv.status_code == 200

        body = rv.json["data"]
        self._token = body.get("token")
        self._user_id = body.get("user_id")
        assert body.get("user_id") != None
        assert body.get("token") != None

    # 测试获取用户信息
    def test_info(self, client):
        token = get_token(client, DEFAULT_LOGIN_PARAMS)
        rv = client.get("/api/user/info", headers={"token": token})
        assert rv.status_code == 200
        body = rv.json["data"]
        assert body.get("email") == self._email
        assert body.get("account_status") == 1
        assert body.get("user_id") != 0

    # 测试修改用户的信息
    def test_change_info(self, client):
        token = get_token(client, DEFAULT_LOGIN_PARAMS)
        nickname = random.choice(["测试1", "测试2", "测试3", "测试4"])
        sex = 1
        phone = '13859943743'
        rv = client.post("/api/user/modify_info",
                         json={
                             "nickname": nickname,
                             "phone": phone,
                             "sex": sex
                         },
                         headers={"token": token})
        print(rv.json)
        assert rv.status_code == 200
        rv = client.get("/api/user/info", headers={"token": token})
        body = rv.json["data"]
        print(body)
        assert body.get("email") == self._email
        assert body.get("account_status") == 1
        assert body.get("user_id") != 0
        assert body.get("nickname") == nickname
        assert body.get("sex") == sex
