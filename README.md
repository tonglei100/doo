![Doo](https://github.com/tonglei100/doo/blob/master/logo.png?raw=true)

# Doo

Doo 是一款简单易用的接口管理解决方案，支持接口文档管理、Mock服务，接口测试等功能。


## 安装

### 初次安装

    pip install doo

### 升级

    pip install -U doo

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

OK，Mock 已经启动起来了。

运行指定的接口文档(如: example.xlsx)，直接带上文件名即可，执行命令如下：

    python app.py example.xlsx


### Postman 测试

doo_example 目录下的 doo.postman_collection.json 为 Postman 用例集

把该文件导入到 Postman 即可对 Mock 进行验证。

> 备注：collection 格式为比较新的2.1版本，请尽量把 Postman 升级到最新版本。


## 接口文档模板

### 模板

example.xlsx

### INDEX 页面

目前采用 Excel 来书写接口文档，其中 INDEX 是基本信息页，提供如下信息：

| Field       | Value                |
| ----------- | -------------------- |
| Title       | EOMS接口文档             |
| Description |                      |
| Version     | 1.0                  |
| BasePath    | <http://example.com> |

注：此网址为虚构，仅作示例

也可以提供全局请求和响应的 Headers

| 请求Headers | 参数名          | 测试数据                              |
| --------- | ------------ | --------------------------------- |
|           | Content-Type | application/x-www-form-urlencoded |
| 响应Headers |              |                                   |
|           | Content-Type | application/json                  |

### 接口页面

除了 INDEX 页面外，其他页面为接口页面。一个接口页面为一组，可以有多个接口页面。
在每个接口页面，需要填写的信息如下：

| 字段   | 值                         |
| ---- | ------------------------- |
| 名称   | 登录                        |
| 描述   | 账号登录接口                    |
| 接口地址 | /api/authentication/login |
| 方法   | POST                      |
| 权限   | None                      |

| 请求     | 参数名      | 中文名称 | 类型     | 是否必传 | 备注     | 测试数据                              |
| ------ | -------- | ---- | ------ | ---- | ------ | --------------------------------- |
|        | account  | 用户名  | string | Y    |        | admin                             |
|        | password | 密码   | string | Y    |        | 123456                            |
| 响应     |          |      |        |      |        | 200                               |
|        | Body     | 报文   | json   | Y    | json格式 | {"code: "0", "message":"success"} |
|        | nickname | 管理员  | string | N    | 用户昵称   | admin                             |
| 测试数据备注 |          |      |        |      |        | 正常场景                              |
