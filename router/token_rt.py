# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request

routes = Blueprint("token", __name__)
# headers = {'Date': 'Thu, 11 Jun 2020 03:56:45 GMT', 'Content-Type': 'application/json;charset=UTF-8', 'Content-Length': '208', 'Connection': 'keep-alive'}
# params = {'system': 'operation-platform', 'timestamp': '1591860425000', 'username': 'op', 'password': '123', 'sign': 'a771df0dad0dc331dcfe723e623de001'}

"""
out:
{'code': 1,
    'message': 'success',
    'data': {
        'accessToken': 'a0ce9bc34fb5453ca0fac3d18c5a0549',
        'refreshToken': '812635f28c374c33b3980aa00446098e',
        'tokenType': 'bearer',
        'expireIn': 86400,
        'scope': 'create'
    },
    'success': True
}
"""

@routes.route("/auth", methods=["POST"])
def get_auth():
    result = {"statusCode": 1, "message": "ok", "data": None, 'success': False}
    params = {}
    for i in request.args:
        params[i] = request.args[i]
    (params)
    a = 1
    return 'a'

# {'code': 1, 'message': 'success', 'data': {'accessToken': 'a0ce9bc34fb5453ca0fac3d18c5a0549', 'refreshToken': '812635f28c374c33b3980aa00446098e', 'tokenType': 'bearer', 'expireIn': 86400, 'scope': 'create'}, 'success': True}

#### 2.1 [post] /auth 用户认证接口
#### 2.2 [get] /checkToken 校验token
#### 2.3 [post] /logout 注销token接口
#### 2.4 [get] /user/getUserInfo 根据用户名等条件查询
#### 2.5 [post] /user/ 添加用户
#### 2.6 [put] /user/ 修改用户
#### 2.7 [get] /user/list 分页查询接口
