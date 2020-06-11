## 接口文档

### 版本变更
时间 | 修改人| 描述
-------------| ------------| ---------------
20190724 | xiangmin.zeng@vistel.cn | v1.0 初始化

### 目录

- [1. 通用说明](#1-通用说明)
    - [1.1 接口授权流程](#11-接口授权流程)
    - [1.2 域名列表](#12-域名列表)
    - [1.3 公共参数](#13-公共参数)
    - [1.4 签名算法](#14-签名算法)
    - [1.5 常见错误码](#15-常见错误码)
- [2. 接口列表](#2-接口列表)
    - [2.1 [post] /auth 用户认证接口](#21-post-auth-用户认证接口) 
    - [2.2 [get] /checkToken 校验token](#22-get-checktoken-校验token)
    - [2.3 [post] /logout 注销token接口](#23-post-logout-注销token接口)
    - [2.4 [get] /user/getUserInfo 根据用户名等条件查询](#24-get-usergetuserinfo-根据用户名等条件查询)
    - [2.5 [post] /user/ 添加用户](#25-post-user-添加用户)
    - [2.6 [put] /user/ 修改用户](#26-put-user-修改用户)
    - [2.7 [get] /user/list 分页查询接口](#27-get-userlist-分页查询接口)

### 1. 通用说明

#### 1.1 接口授权流程
- 申请应用，得到密钥
- 调用认证接口获取token
- 调用校验接口验证token

#### 1.2 域名列表
环境 | 域名
-------------| ------------
测试环境 | https://t-oauth.vistel.cn 
正式环境 | https://oauth.vistel.cn

#### 1.3 公共参数

[ 请求任意接口，除特别说明外，以下所有请求接口均需要加上公共参数 ]

名称 | 类型 | 是否必须| 描述 | 示例
------- | ------- | ---- |  ----  | ------ 
system | string | 是 | 系统代号 | bss
timestamp | number | 是 | UTC1970年01月01日00时00分00秒到现在的毫秒数 | 1563950122930
sign | string  | 是 | 签名, 签名算法另见1.4章节 | cd6582dac98d476fc8fd191a55c96f0b

[ 接口返回，除特别说明外，以下所有请求接口均返回以下结构的application/json类型 ]

名称 | 类型 | 描述 | 示例
------- | ------- | ---- |  ----
code | number | 返回码 |  1 
success | boolean  | 默认1为成功, 其他为失败 | true
message | string  | 失败返回的信息 | password is required
data | object  | 具体属性见各个API返回参数说明 | {"token" : "x509..."}

#### 1.4 签名算法

为防止API调用被篡改，或抓包回放，固调用每一个API都要携带签名，服务端会对签名进行验证，
不合法的请求将会被拒绝。举起签名过程如下：
- 对所有API请求参数（包含公共参数和业务参数），根据参数名称的ASCII码表的顺序排序。
如：foo=1&bar=2&foo_bar=3&foobar=4排序后的顺序是bar=2&foo=1&foo_bar=3&foobar=4;
- 将排序好的参数名和参数值拼装在一起，根据上面的示例得到的结果为：bar2foo1foo_bar3foobar4;
- 把拼装好的字符串采用utf-8编码，使用签名算法对编码后的字节流进行摘要;
- 默认使用MD5算法，需要在拼装的字符串后加上app的secret后，再进行摘要，如：md5(secret + bar2foo1foo_bar3foobar4 + to_string(body) +secret)；
- 将摘要得到的字节流结果使用十六进制表示，如：hex("hello world".getBytes("utf-8")) = "68656C6C6F776F726C64";
- 说明：MD5是128位长度的摘要算法，用16进制表示，一个十六进制的字符能表示4个位，所以签名后的字符串长度固定为32个十六进制字符;

**JAVA签名示例代码**
```java
public static String signTopRequest(Map<String, String> params, String body, String secret, String signMethod) throws IOException {
	// 第一步：检查参数是否已经排序
	String[] keys = params.keySet().toArray(new String[0]);
	Arrays.sort(keys);

	// 第二步：把所有参数名和参数值串在一起
	StringBuilder query = new StringBuilder(secret);
	for (String key : keys) {
		String value = params.get(key);
		if (StringUtils.areNotEmpty(key, value)) {
			query.append(key).append(value);
		}
	}

	// 第三步：使用MD5加密
    query.append(body).append(secret);
    byte[] bytes = encryptMD5(query.toString());

	// 第四步：把二进制转化为大写的十六进制
	return byte2hex(bytes);
}

public static byte[] encryptMD5(String data) throws IOException {
	return encryptMD5(data.getBytes(Constants.CHARSET_UTF8));
}

public static String byte2hex(byte[] bytes) {
	StringBuilder sign = new StringBuilder();
	for (int i = 0; i < bytes.length; i++) {
		String hex = Integer.toHexString(bytes[i] & 0xFF);
		if (hex.length() == 1) {
			sign.append("0");
		}
		sign.append(hex);
	}
	return sign.toString();
}
```

**PYTHON签名示例代码**
```python
import time
import json
import hashlib
import copy
import random
import string
from requests import request


def get_sign(param, body, app_secret):
    sorted_params = sorted(param.items(), key=lambda x: x[0])
    encodestring = secret
    for k, v in sorted_params:
        encodestring += (k + str(v))

    encodestring += (body + app_secret)

    m = hashlib.md5()
    m.update(encodestring.encode('utf-8'))
    sign = m.hexdigest()

    # print('签名前：' + encodestring)
    # print('签名后：' + sign)

    return sign


def genRandomString(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))


system = 'operation-platform'
secret = '6g7srQ73QatzQrFx'

base_params = {
    'system': system,
    'timestamp': str(int(time.time()) * 1000)
}

getUserInfoRequestURL = 'https://t-oauth.vistel.cn/user/getUserInfo'
params = copy.deepcopy(base_params)
params['id'] = str(30001)
params['sign'] = get_sign(params, '', secret)

response = request('GET', getUserInfoRequestURL, params=params)
print(response.json())

addUserInfoRequestURL = 'https://t-oauth.vistel.cn/user/'
headers = {"Content-Type": "application/json;charset=utf-8"}
payload = {
    "username": "just_" + genRandomString(),
    "password": "qwerty",
    "gender": "M",
    "phone": "18578437843",
    "system": system
}
params = copy.deepcopy(base_params)
params['sign'] = get_sign(params, json.dumps(payload), secret)
response = request('POST', addUserInfoRequestURL, params=params, data=json.dumps(payload), headers=headers)
print(response.json())



```

#### 1.5 常见返回码说明

code | 含义
------- |  ------
0 | 失败
1 | 正确
10 | 缺少必要参数
32 | 记录不存在
100 | 系统错误
1004001 | 账号密码不匹配
1004002 | 签名不正确
1005001 | token不存在
1005002 | 用户未授权
1005003 | 账号锁定
1005004 | 账号重复

### 2. 接口列表

#### 2.1 [post] /auth 用户认证接口

输入参数：

名称 | 类型 | 是否必须 | 描述
------- | ------- | ---- |  ----
username | string | 是  | 用户账号
password | string | 是  | 用户密码

输出参数：

名称 | 类型 | 描述 
------ | ------ | --------
accessToken | String | token
expireIn | number | 失效时间，单位秒

请求示例:
```http request
POST /auth HTTP/1.1
Host: $HOST
Content-Type: application/x-www-form-urlencoded

username=admin&password=cscjglymm607&system=anno&timestamp=1563950122930&sign=cd6582dac98d476fc8fd191a55c96f0b
```

响应示例：
```json
{
    "code": 1,
    "success": true,
    "data": {
        "accessToken": "43f1c86be28a4796bb973b31cf95f042",
        "expireIn": 3600
    }
}
```
```json
{
    "code": 32,
    "success": false,
    "message": "record not exist",
    "data": null
}
```

#### 2.2 [get] /checkToken 校验token

输入参数：

名称 | 类型 | 是否必须 | 描述 | 示例
------- | ------- | ---- |  ----  | ------ 
Authorization | Header | 是 | 在header上写入accessToken的值 | e.g. Authorization: "Bearer 43f1c86be28a4796bb973b31cf95f042"

输出参数：

名称 | 类型 | 描述 
------ | ------ | --------
id | number | user id
username | string | 用户账号
nickName | string | 别名
realName | string | 真实姓名
phone | string | 电话
email | string | 邮箱
gender | string | 性别, M:男;F:女
avatar | string | 头像
status | string | 状态 0:失效;1:正常
createTime | string | 创建时间, java: yyyy-MM-dd'T'HH:mm:ss.SSSZ, python: %Y-%m-%dT%H:%M:%S.%f%z
updateTime | string | 最新修改时间
version | string | 版本号

请求示例：
```http request
GET /checkToken?system=anno&timestamp=123456789&sign=cd6582dac98d476fc8fd191a55c96f0b HTTP/1.1
Host: $HOST
Authorization: Bearer 41d3529d6ea042709206e9beb6bf6fc9
```

响应示例：
```json
{
	"code": 1,
	"data": {
        "id": 30001,
        "username": "admin",
		"email": "",
		"gender": "M",
		"nickName": "",
		"phone": "",
		"realName": "管理员",
		"status": 1,
		"createTime": "2017-06-06T21:01:27.000+0800",
        "updateTime": "2019-07-17T11:54:58.000+0800",
		"version": 2
	},
	"success": true
}
```

#### 2.3 [post] /logout 注销token接口

输入参数：

名称 | 类型 | 是否必须 | 描述 | 示例
------- | ------- | ---- |  ----  | ------ 
Authorization | Header | 是 | 在header上写入accessToken的值 | e.g. Authorization: "Bearer qwerty"

输出参数：

名称 | 类型 | 描述 
------ | ------ | --------
 无 |  | 无特殊返回字段

请求示例：
```http request
POST /logout?system=anno&timestamp=123456789&sign=cd6582dac98d476fc8fd191a55c96f0b HTTP/1.1
Host: $HOST
Authorization: Bearer 41d3529d6ea042709206e9beb6bf6fc9
```

响应示例：
```json
{
	"code": 1,
	"data": null,
	"success": true
}
```

#### 2.4 [get] /user/getUserInfo 根据用户名等条件查询

输入参数：

名称 | 类型 | 是否必须 | 描述
------- | ------- | ---- |  ----
id | number | 二选一 | user id
username | string | 二选一  | 开放平台获取的授权码

输出参数：

名称 | 类型 | 描述 
------ | ------ | --------
id | number | user id
username | string | 用户账号
nickName | string | 别名
realName | string | 真实姓名
phone | string | 电话
email | string | 邮箱
gender | string | 性别, M:男;F:女
avatar | string | 头像
status | string | 状态 0:失效;1:正常
createTime | string | 创建时间, java: yyyy-MM-dd'T'HH:mm:ss.SSSZ, py: %Y-%m-%dT%H:%M:%S.%f%z
updateTime | string | 最新修改时间
version | string | 版本号

请求示例：
```http request
GET /user/getUserInfo?id=30001&system=bss&timestamp=1564048255089&sign=d11a5439073536d5886b05b7540a6515 HTTP/1.1
Host: $HOST
```

响应示例：
```json
{
	"code": 1,
	"data": {
        "id": 30001,
        "username": "admin",
		"email": "",
		"gender": "M",
		"nickName": "",
		"phone": "",
		"realName": "管理员",
		"status": 1,
		"createTime": "2017-06-06T21:01:27.000+0800",
        "updateTime": "2019-07-17T11:54:58.000+0800",
		"version": 2
	},
	"success": true
}
```

#### 2.5 [post] /user/ 添加用户

输入参数：

名称 | 类型 | 是否必须 | 描述
------ | ------ | -------- | --------
username | string | 是 | 用户账号, 全平台唯一
password | string | 是 | 用户密码
nickName | string| 否  | 别名
realName | string| 否  | 真实姓名
phone | string | 是 | 电话
email | string| 否  | 邮箱
gender | string| 是  | 性别, M:男;F:女
status | string | 否 | 状态 0:失效;1:正常, 默认1
system | string| 是 | 冗余字段,开通用户系统权限, 与公共参数含义不同

输出参数：

名称 | 类型 | 描述 
------ | ------ | --------
id | number | user id
username | string | 用户账号
nickName | string | 别名
realName | string | 真实姓名
phone | string | 电话
email | string | 邮箱
gender | string | 性别, M:男;F:女
avatar | string | 头像
status | string | 状态 0:失效;1:正常
createTime | string | 创建时间, java: yyyy-MM-dd'T'HH:mm:ss.SSSZ, py: %Y-%m-%dT%H:%M:%S.%f%z
updateTime | string | 最新修改时间
version | string | 版本号

请求示例：
```http request
POST /user/?system=bss&timestamp=1564050220043&sign=ee22aa7666465714460d71aa7dbcfcad HTTP/1.1
Host: $HOST
Content-Type: application/json

{
	"username":"just",
	"password":"qwerty",
	"gender":"M",
	"phone":"18578437843",
	"system":"bss"
}
```

响应示例：
```json
{
    "code": 1,
    "message": null,
    "data": {
        "id": 30357,
        "username": "just",
        "nickName": null,
        "realName": null,
        "phone": "18578437843",
        "email": null,
        "gender": "M",
        "status": 1,
        "createTime": "2019-07-24T18:24:00.187+0800",
        "updateTime": "2019-07-24T18:24:00.187+0800",
        "version": 1
    },
    "success": true
}
```

#### 2.6 [put] /user/ 修改用户

输入参数：

名称 | 类型 | 是否必须 | 描述
------ | ------ | -------- | --------
id | number | 是 | 用户id
password | string | 是 | 用户密码
nickName | string| 否  | 别名
realName | string| 否  | 真实姓名
phone | string | 是 | 电话
email | string| 否  | 邮箱
gender | string| 是  | 性别, M:男;F:女
status | string | 否 | 状态 0:失效;1:正常, 默认1
system | string| 是 | 冗余字段, 用户系统权限, 与公共参数含义不同

输出参数：

名称 | 类型 | 描述 
------ | ------ | --------
无 | |

请求示例：
```http request
PUT /user/?system=bss&timestamp=1564110711854&sign=9a40fb9a22bdc73c907ddba5a1a82906 HTTP/1.1
Host: $HOST
Content-Type: application/json

{
	"id": 30001,
	"password": "123456",
	"system": "bss"
}
```

响应示例：
```json
{
    "code": 1,
    "message": null,
    "data": {
        "id": 30001,
        "username": "admin",
        "systemCode": 4
    },
    "success": true
}
```

#### 2.7 [get] /user/list 分页查询接口

输入参数：

名称 | 类型 | 是否必须 | 描述
------ | ------ | -------- | --------
offset | string | 否 | 页码, 从0开始默认0
limit | string| 否  | 页宽, 默认10
sort | string | 否 | 排序字段, 默认为"id"
orderBy | string| 否  | 排序, 可选ASC/DESC, 默认ASC
search | string| 否  | 模糊匹配字段, 默认搜索username,nickName, phone
system | string| 是  | 用户所属系统

输出参数：

名称 | 类型 | 描述 
------ | ------ | --------
total | number | 此分页条件下总条数
rows | array | 用户信息详细字段见上一节

请求示例：
```http request
GET /user/list?offset=0limit=15&system=bss&timestamp=1564112377802&sign=4070fbb25ae5877d87ea3ba0edb8e0bb HTTP/1.1
Host: $HOST
```

响应示例：
```json
{
    "code": 1,
    "data": {
        "total": 6,
        "rows": [
            {
                "id": 30001,
                "username": "admin",
                "nickName": "",
                "realName": "管理员",
                "phone": "17512312445",
                "email": "mmm@vistel.cn",
                "gender": "M",
                "avatar": "",
                "status": 1,
                "lastLoginIp": "",
                "createTime": "2017-06-06T21:01:27.000+0800",
                "updateTime": "2019-07-25T11:19:01.000+0800",
                "version": 29
            }
        ]
    },
    "success": true
}
```
