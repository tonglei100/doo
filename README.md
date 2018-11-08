![Doo](https://github.com/tonglei100/doo/blob/master/logo.png?raw=true)

# Doo

Doo 是一款简单易用的接口管理解决方案，支持接口文档管理、Mock服务，接口测试等功能。接口文档采用 yaml 或 Excel 格式书写，简单快捷，Mock 基于该文档，无需数据库，一条命令秒变 Mock 服务。


## 关注

Doo 是 Sweetest 的姊妹项目，所以 QQ 交流群和微信公众号合并到 Sweetest ，欢迎加入：

微信公众号：安装、配置、使用的详细图文说明，最新版本发布更新说明

QQ 交流群：158755338 (验证码：python)

扫描**公众号**及**QQ群**二维码加入我们

![Doo](https://github.com/tonglei100/sweetest/blob/master/snapshot/sweetest.jpg?raw=true)


## 安装

### 初次安装

```shell
pip install doo
```

### 升级

```shell
pip install -U doo
```

### Apistar 版本说明

Doo 在底层选择了 Apistar 作为 Web 框架，但 Apistar 从 0.6.0 开始转型为 api 工具，不再兼容原有功能；
所以，如果 Apistar 已经为 0.6.0，请用如下命令降级：

```shell
pip install -U "apistar<0.6.0"
```

## 快速体验

### Mock

在合适的目录，如 D:\\doo 目录下，打开 CMD 命令行窗口，输入如下命令

```shell
doo
cd doo_example
python app.py
```

如果看到如下信息

```shell
* Restarting with stat
* Debugger is active!
* Debugger PIN: 248-052-080
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

OK，示例 Mock 已经启动起来了。

对接口文档启动 Mock 有3种方式：

1. 运行 Excel 接口文档(如: example.xlsx)，直接带上文件名即可，执行命令如下：

    python app.py example.xlsx

2. 运行 yaml 接口文档(如: example.yml)，执行命令如下：

    python app.py example.yml

3. 运行指定目录下的所有 yaml 接口文档(如: D:\\doc)，执行命令如下：

    python app.py D:\\doc


### Postman 测试

doo_example 目录下的 doo.postman_collection.json 为 Postman 用例集

把该文件导入到 Postman 即可对示例 Mock 进行验证。

> 备注：collection 格式为比较新的2.1版本，请尽量把 Postman 升级到最新版本。


## 接口文档模板

### 1. yaml 模板

example.yml

#### 模板格式

```yaml
--- # 通用描述
Title: Example 接口文档
Description: ''
Version: '1.0'
BasePath: http://example.com
REQUEST_Headers:
  Content-Type: application/json
RESPONSE_Headers:
  Content-Type: application/json

---  # 接口描述
Name: LOGIN
Desc: 账号登录
Path: /api/authentication/login
Method: POST
GROUP: USER
Auth: None

REQUEST:
  Headers:
    Content-Type: application/json
  Body:
    # 参数名: [类型, 是否必传, 中文名称, 备注]
    account: [string, Y, 用户名, 手机号/邮箱]
    password: [string,Y, 密码, 6~12位数字字母组合]

RESPONSE:
  Headers:
    Content-Type: application/json
  Body:
    # json 支持多层嵌套
    Body: {code: [string, Y, 错误码, 报文里的错误码], message: [string, Y, 提示信息, 出错时信息]}
    nickname: [string, N, 昵称, 用户昵称]

# 以下为 Mock 测试数据，根据需要填写
DATA1:
  REQUEST:
    account: admin
    password: '123456'
  RESPONSE:
    code: '0'
    message: success
    nickname: admin
  status_code: 200  #可选，默认为 200
  delay: 0.5  #可选，默认为 0
  remark: admin 账户登录  #可选，默认为 ''
```

备注：对单个或多个 yaml 接口文档启动 Mock 时，通用描述部分，只能有1个，如果有多个，则只有最后被读取的那个有效。


### 2. Excel 模板

example.xlsx

#### INDEX 页面

目前采用 Excel 来书写接口文档，其中 INDEX 是基本信息页，提供如下信息：

| Field       | Value                |
| ----------- | -------------------- |
| Title       | EOMS接口文档          |
| Description |                      |
| Version     | 1.0                  |
| BasePath    | <http://example.com> |

注：此网址为虚构，仅作示例

也可以提供全局请求和响应的 Headers

| Request Headers | 参数名          | 测试数据                       |
| --------------- | ------------ | --------------------------------- |
|                 | Content-Type | application/x-www-form-urlencoded |
| Response Headers|              |                                   |
|                 | Content-Type | application/json                  |

#### 接口页面

除了 INDEX 页面外，其他页面为接口页面。一个接口页面为一组，可以有多个接口页面。
在每个接口页面，需要填写的信息如下：

| 字段   | 值                         |
| ------ | -------------------------- |
| 名称   | 登录                       |
| 描述   | 账号登录接口               |
| 接口   | /api/authentication/login |
| 方法   | POST                       |
| 权限   | None                       |

| 请求   | 参数名   | 中文名称 | 类型   | 是否必传| 备注   | 测试数据                          |
| ------ | -------- | -------- | ------ | ------- | ------ | --------------------------------- |
|        | account  | 用户名   | string | Y       |        | admin                             |
|        | password | 密码     | string | Y       |        | 123456                            |
| 响应   |          |          |        |         |        | 200                               |
|        | Body     | 报文Body | json   | Y       |json格式| {"code: "0", "message":"success"} |
|        | nickname | 昵称     | string | N       |用户昵称| admin                             |
| 响应延时|          |          |        |         |        | 0.5                               |
| 测试数据备注 |    |          |        |         |        | 正常场景                          |


### 特殊匹配

#### 模糊值匹配

请求字段为星号(*)，则该字段匹配任意值(包括无该字段)，如

```yaml
DATA1:
  REQUEST:
    account: guess
    password: '*'
  RESPONSE:
    code: '0'
    message: success
    nickname: guess
```
则请求中，只要 account 为 guess，则匹配成功，返回该条响应数据

Excel 格式的测试数据也一样。

如果请求字段的值本来就是星号(*)，则测试数据需要转义为'\\\*'，相应的，如果请求字段的值本来就是'\\'开头,则测试数据要写'\\\\'

如果要匹配该接口的所有请求，则可以把请求字段都设置为星号(*)，如：

```yaml
DATA1:
  REQUEST:
    account: '*'
    password: '*'
  RESPONSE:
    code: '0'
    message: success
    nickname: anyone
```
在 Mock 时，会优先匹配有明确值的 DATA，星号(*)越多的 DATA 越靠后匹配。

#### 其他匹配

|开头字符|匹配说明|示例    |示例说明    | 备注
|------|------|--------|-----------| -------------------|
| \*   |包含   |*test   |包含test    | 和单独的星号(*)不同      |
| ^    |开头   | ^hello |以hello开头 |
| $    |结尾   | $world |以world结尾 |
| -    |无此字段| -      |必须无此字段 |
| +    |有此字段| +      |必须有此字段 |值可以为任意值       |
