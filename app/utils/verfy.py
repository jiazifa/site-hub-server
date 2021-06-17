from typing import Any
from flask import request, session
from .params_helper import parse_params_from_request

def get_user_from_request_if_could() -> Any:
    from app.model import User

    params = parse_params_from_request()
    alise: str = "token"
    token = params.get(alise)
    if not token:
        token = session.get(alise)
    if not token:
        token = request.cookies.get(alise)
    if not token:
        return None
    user = User.get_user(token=token)
    return user
