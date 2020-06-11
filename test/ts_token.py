# -*- coding: utf-8 -*-
import time
import json
import hashlib
import copy
import random
import string
from requests import request
from ConfigHelper.ConfigHelper import ConfigHelper
from urllib.parse import urljoin
import requests, unittest

config = ConfigHelper()

class oauth(object):
# class Test_user(unittest.TestCase):
    # def setUp(self):
    def __init__(self, access_token, username, password):
        self.system = config.ConfigSectionMapCompatiable('AUTH_CONFIG', 'SYSTEM')
        self.secret = config.ConfigSectionMapCompatiable('AUTH_CONFIG', 'SECRET')
        # self.host = config.ConfigSectionMapCompatiable('AUTH_CONFIG', 'HOST')
        self.host_url = "http://localhost:3050"
        self.accessToken = ''
        self.username = 'op'
        self.password = '123'
        self.base_params = {
            'system': self.system,
            'timestamp': str(int(time.time()) * 1000)
        }

    def get_sign(self, param, body, app_secret):
        sorted_params = sorted(list(param.items()), key=lambda x: x[0])
        encodestring = self.secret
        for k, v in sorted_params:
            encodestring += (k + str(v))

        encodestring += (body + app_secret)

        m = hashlib.md5()
        m.update(encodestring.encode('utf-8'))
        sign = m.hexdigest()

        # print('签名前：' + encodestring)
        # print('签名后：' + sign)

        return sign

    @staticmethod
    def genRandomString(slen=10):
        return ''.join(random.sample(string.ascii_letters + string.digits, slen))

    '''

    {

        "message":null,
        "code":1,
        "data":{
            "expireIn":3600,
            "refreshToken":"089ebc5f35d64850b6c21ed3287893c1",
            "tokenType":"bearer",
            "accessToken":"04dec8e688774333b523076f9cdf5f33",
            "scope":"create"
        },
        "success":true

    }

    '''

    def auth(self):
        headers = {"Content-Type": "application/json;charset=utf-8"}
        params = copy.deepcopy(self.base_params)

        params['username'] = self.username
        params['password'] = self.password
        payload = {}
        params['sign'] = self.get_sign(params, json.dumps(payload), self.secret)
        rst = requests.post(self.host_url + "/api/token/auth", params=params, headers=headers)
        # print(json.dumps(response.json(), ensure_ascii=False))

        return rst.json()

    '''

    {

        "message":null,
        "code":1,
        "data":{
            "username":"zhangbing",
            "status":1,
            "updateTime":"2019-07-26T10:59:44.000+0800",
            "realName":null,
            "lastLoginIp":"",
            "gender":"M",
            "createTime":"2019-07-26T10:59:44.000+0800",
            "id":100077,
            "phone":"18578437843",
            "systemCode":32,
            "version":1,
            "avatar":null,
            "nickName":null,
            "email":null,
            "statusJson":null
        },
        "success":true

    }

    '''

    # def checkToken(self):
    #     checkurl = urljoin(self.host, '/checkToken')
    #     headers = {"Authorization": "Bearer "}
    #     headers["Authorization"] = "Bearer " + self.accessToken
    #     params = copy.deepcopy(self.base_params)
    #
    #     params['sign'] = self.get_sign(params, '', self.secret)
    #     response = request('GET', checkurl, params=params, headers=headers)
    #     # print(json.dumps(response.json(), ensure_ascii=False))
    #     ret = response.json()
    #     if ret['code'] == 1:
    #         return ret['data']
    #     else:
    #         return None
    #
    # def getUserInfo(self):
    #     tp_url = urljoin(self.host, 'user/getUserInfo')
    #     params = copy.deepcopy(self.base_params)
    #     params['username'] = self.username
    #     params['sign'] = self.get_sign(params, '', self.secret)
    #
    #     response = request('GET', tp_url, params=params)
    #     # print(json.dumps(response.json(), ensure_ascii=False))
    #     return response.json()
    #
    # def addUser(self, gender, phone, email, realname):
    #     url = urljoin(self.host, '/user/')
    #     headers = {"Content-Type": "application/json;charset=utf-8"}
    #     payload = {
    #         "username": self.username,
    #         "password": self.password,
    #         "gender": gender,
    #         "phone": phone,
    #         "email": email,
    #         "realName": realname,
    #         "system": self.system
    #     }
    #     params = copy.deepcopy(self.base_params)
    #     params['sign'] = self.get_sign(params, json.dumps(payload), self.secret)
    #     response = request('POST', url, params=params, data=json.dumps(payload), headers=headers)
    #     # print(json.dumps(response.json(), ensure_ascii=False))
    #     return response.json()
    #
    # '''
    #
    # {
    #
    #     "message":null,
    #     "code":1,
    #     "data":{
    #         "rows":[
    #             {
    #                 "username":"just_tniQawIgdC",
    #                 "status":1,
    #                 "updateTime":"2019-07-26T10:56:21.000+0800",
    #                 "realName":null,
    #                 "lastLoginIp":"",
    #                 "gender":"M",
    #                 "createTime":"2019-07-26T10:56:21.000+0800",
    #                 "id":100076,
    #                 "phone":"18578437843",
    #                 "systemCode":32,
    #                 "version":1,
    #                 "avatar":null,
    #                 "nickName":null,
    #                 "email":null,
    #                 "statusJson":null
    #             },
    #             {
    #                 "username":"zhangbing",
    #                 "status":1,
    #                 "updateTime":"2019-07-26T10:59:44.000+0800",
    #                 "realName":null,
    #                 "lastLoginIp":"",
    #                 "gender":"M",
    #                 "createTime":"2019-07-26T10:59:44.000+0800",
    #                 "id":100077,
    #                 "phone":"18578437843",
    #                 "systemCode":32,
    #                 "version":1,
    #                 "avatar":null,
    #                 "nickName":null,
    #                 "email":null,
    #                 "statusJson":null
    #             }
    #         ],
    #         "total":18
    #     },
    #     "success":true
    #
    # }
    #
    # '''
    #
    # def getUserList(self, offset, limit):
    #     url = urljoin(self.host, '/user/list')
    #     params = copy.deepcopy(self.base_params)
    #     params['offset'] = str(offset)
    #     params['limit'] = str(limit)
    #     params['sort'] = "id"
    #     params['orderBy'] = "DESC"
    #     params['sign'] = self.get_sign(params, '', self.secret)
    #     response = request('GET', url, params=params)
    #     return response.json()
    #
    # def logout(self):
    #     authurl = urljoin(self.host, '/logout')
    #     headers = {"Authorization": "Bearer "}
    #     headers["Authorization"] = "Bearer " + self.accessToken
    #     params = copy.deepcopy(self.base_params)
    #
    #     payload = {}
    #     params['sign'] = self.get_sign(params, json.dumps(payload), self.secret)
    #     response = request('POST', authurl, params=params, data=json.dumps(payload), headers=headers)
    #     # print(json.dumps(response.json(), ensure_ascii=False))
    #
    #     return response.json()
    #
    # def getUserInfoById(self, id):
    #     tp_url = urljoin(self.host, 'user/getUserInfo')
    #     params = copy.deepcopy(self.base_params)
    #     params['id'] = id
    #     params['sign'] = self.get_sign(params, '', self.secret)
    #     response = request('GET', tp_url, params=params)
    #     # print(json.dumps(response.json(), ensure_ascii=False))
    #     return response.json()
    #
    # def updateUser(self, gender, phone, email, realname, user_id):
    #     addUserInfoRequestURL = urljoin(self.host, '/user/')
    #     headers = {"Content-Type": "application/json;charset=utf-8"}
    #     payload = {
    #         "id": user_id,
    #         "username": self.username,
    #         "gender": gender,
    #         "phone": phone,
    #         "email": email,
    #         "realName": realname,
    #         "system": self.system
    #     }
    #     params = copy.deepcopy(self.base_params)
    #     params['sign'] = self.get_sign(params, json.dumps(payload), self.secret)
    #
    #     response = request('PUT', addUserInfoRequestURL, params=params, data=json.dumps(payload), headers=headers)
    #     # print(json.dumps(response.json(), ensure_ascii=False))
    #     return response.json()
    #


if __name__ == '__main__':
    oauth2 = oauth("", 'op', '123')
    result = oauth2.auth()
    # unittest.main()