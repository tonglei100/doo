# doo

## 接口文档模板

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

示例见 doo.xlsx

## 接口文档解析

```python
python doo.py
```
