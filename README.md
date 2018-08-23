# doo

## 接口文档模板

模板：doo.xlsx

### INDEX 页面

目前采用 Excel 来书写接口文档，其中 INDEX 是基本信息页，提供如下信息：

| Field       | Value             |
| ----------- | ----------------- |
| Title       | EOMS接口文档          |
| Description |                   |
| Version     | 1.0               |
| BasePath    | <http://emos.com> |

也可以提供全局请求和响应的 Headers

| 请求Headers | 参数名          | 测试数据                              |
| --------- | ------------ | --------------------------------- |
|           | Content-Type | application/x-www-form-urlencoded |
| 响应Headers |              |                                   |
|           | Content-Type | application/json                  |


### 接口页面

除了 INDEX 页面外，其他页面为接口页面。一个接口页面为一组，可以有多个接口页面。
在每个接口页面，需要填写的信息如下：

|字段  |值                         |
|----|----------------------------|
|名称  |登录                       |
|描述  |账号登录接口                 |
|接口地址|/api/authentication/login |
|方法  |POST                       |
|权限  |None                       |


|请求    |参数名     |中文名称|类型    |是否必传|备注    |测试数据                 |
|------|--------|----|------|----|------|-----------------------------------|
|      |account |用户名 |string|Y   |      |admin                            |
|      |password|密码  |string|Y   |      |123456                            |
|响应    |        |    |      |    |      |200                               |
|      |Body    |报文  |json  |Y   |json格式|{"code: "0", "message":"success"}|
|      |nickname|管理员 |string|N   |用户昵称  |admin                          |
|测试数据备注|        |    |      |    |      |正常场景                         |



## 接口文档解析

```python
python doo.py
```
