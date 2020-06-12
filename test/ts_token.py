# -*- coding: utf-8 -*-
import unittest, requests, copy, hashlib, time, json
from ConfigHelper.ConfigHelper import ConfigHelper

config = ConfigHelper()

class Test_user(unittest.TestCase):
    # before
    def setUp(self):
        print('Case Before')
        self.system = config.ConfigSectionMapCompatiable('AUTH_CONFIG', 'SYSTEM')
        self.secret = config.ConfigSectionMapCompatiable('AUTH_CONFIG', 'SECRET')
        self.headers = {"Content-Type": "application/json;charset=utf-8"}
        self.host_url = "http://localhost:3060"
        self.base_params = {
            'system': self.system,
            'timestamp': str(int(time.time()) * 1000)
        }
        print('Case Before')
        pass

    def get_sign(self, param, body, app_secret):
        sorted_params = sorted(list(param.items()), key=lambda x: x[0])
        encodestring = self.secret
        for k, v in sorted_params:
            encodestring += (k + str(v))

        encodestring += (body + app_secret)

        m = hashlib.md5()
        m.update(encodestring.encode('utf-8'))
        sign = m.hexdigest()

        print('签名前：' + encodestring)
        print('签名后：' + sign)

        return sign

    def test_get_auth(self):
        # payload = '{"user": "op", "pwd": "123"}'
        params = copy.deepcopy(self.base_params)
        params['username'] = 'op'
        params['password'] = '123'
        payload = {}
        params['sign'] = self.get_sign(params, json.dumps(payload), self.secret)
        req = requests.post(self.host_url + "/api/token/auth", params=params, data=json.dumps(payload), headers=self.headers)
        user_list = req.json()
        print(user_list)
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
if __name__ == '__main__':
    unittest.main()

