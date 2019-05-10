![Doo](https://doc.sweeter.io/docs/_media/doo.png)

# Doo

Doo 是一款简单易用的接口管理解决方案，支持接口文档管理、Mock服务，接口测试等功能。接口文档采用 yaml 或 Excel 格式书写，简单快捷，Mock 基于该文档，无需数据库，一条命令秒变 Mock 服务。

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

> 详细文档：https://doc.sweeter.io/doo/

## 加入我们

QQ 交流群：**158755338**
> (验证码：python) <small>注意首字母小写</small>

微信公众号：**喜文测试**

![QQ2](https://doc.sweeter.io/docs/_media/QQ.png)![WeChat](https://doc.sweeter.io/docs/_media/WeChat.png)