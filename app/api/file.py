import os
from typing import List, Union
from uuid import uuid4

from flask import Blueprint, Flask, current_app, request
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.utils import secure_filename

from app.utils import response_success
from app.utils.errors import ParameterException, UnknownExeception

prefix: str = "file"
api = Blueprint(prefix, __name__)


def upload_floder(app: Flask) -> Union[str, None]:
    return app.config.get("UPLOAD_FLODER")

def upload():
    files: List[FileStorage] = []
    file_dict: ImmutableMultiDict = request.files
    
    if file_dict.getlist("files"):
        tfs: List[FileStorage] = file_dict.get("files") or []
        files.extend(tfs)
    elif file_dict.get("file"):
        tf: Union[FileStorage, None] = file_dict.get("file")
        if tf:
            files.append(tf)
    else:
        raise ParameterException(message="至少上传一个文件")
    
    dest: str = upload_floder(current_app)
    if not dest:
        raise UnknownExeception(message="当前缺少关键配置，服务不可用")
    if not os.path.exists(dest):
        os.mkdir(dest)
    payload: List[Dict[str, str]] = []
    for file in files:
        filename: str = secure_filename(file.filename)
        # 拓展名
        extension: str = filename.split(".")[-1].lower()
        # uuid
        identifier = str(uuid4()).replace("-", "")
        target_file = ".".join([identifier, extension])
        file.save(os.path.join(dest, target_file))
        url = "/".join(["/shared", target_file])
        full_url = request.scheme + "://" + request.host + url
        payload.append({
            "full_path": full_url,
            "target": target_file,
            "target_url": url,
            "source": filename
        })
    return response_success(body=payload)


def setup_urls(api: Blueprint):
    api.add_url_rule("/upload/", view_func=upload, methods=["POST"])


setup_urls(api)