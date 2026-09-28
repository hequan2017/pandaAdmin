[简体中文](README.md) | [English](README.en.md)

# pandaAdmin 熊猫后端

> 作者: 何全，github地址: <https://github.com/hequan2017> ，QQ交流群: 620176501

> 通过此教程完成从零入门，能够独立编写一个简单的 CMDB 系统。

> 目前主流的开发方式分为 2 种：MVC 和 MVVC 方式。本项目提供 MVC 方式和 MVVC（前后端分离）的入门教程。

## 项目介绍

pandaAdmin（熊猫）是《Django之入门 CMDB系统》系列教程的配套项目：基于 Django 2.2 + DRF 3.10 + MySQL，采用 CBV 编程方式，实现 Token 登录认证、用户信息接口和一个完整的增删改查示例（test 表），并自带 API 文档与 Django Admin 后台，供前端项目 [panda](https://github.com/hequan2017/panda) 调用。适合想从零入门 Django Web / CMDB 开发的同学。

## 📖 教程目录

![DEMO](doc/images/demo1.png)
![DEMO](doc/images/2-1.png)

[Django之入门 CMDB系统  (一) 基础环境](doc/1.md)

[Django之入门 CMDB系统  (二) 前端模板](doc/2.md)

[Django之入门 CMDB系统  (三) 登录注销](doc/3.md)

[Django之入门 CMDB系统  (四) 增删改查](doc/4.md)

[Django之入门 CMDB系统  (五) 前后端分离之前端](doc/5.md)

[Django之入门 CMDB系统  (六) 前后端分离之后端](doc/6.md)

## ✨ 功能特性

- Token 认证：`/token` 获取 DRF Token，支持 Basic / Token / Session 三种认证方式
- 接口：`/system/user_info` 用户信息、`/system/logout` 注销、`/system/test` 与 `/system/test/{id}` 增删改查示例
- 自动 API 文档：`/docs`（带 web 调试界面，可在 settings 中关闭）
- Django Admin 后台：`/admin`；自定义 Users 模型继承 AbstractUser（扩展职位、头像、手机号字段）
- CORS 跨域支持（django-cors-headers），方便前后端分离联调
- 附 Kubernetes 部署示例 yaml（`system/k8s/` 目录）

## 🛠 技术栈

- MVC / MVVC 模式，CBV 编程方式
- CentOS 7.6、Python 3.6、Django 2.2、MySQL 5.7、PyCharm 2019.2（Windows 远程 CentOS 开发）
- DRF 3.10.3、django-cors-headers、celery 4.3、mysqlclient（完整依赖见 `requirements.txt`）

## 🚀 快速开始

```bash
git clone https://github.com/hequan2017/pandaAdmin.git
cd pandaAdmin
pip3 install -r requirements.txt

# 修改 pandaAdmin/settings.py 中 DATABASES 的 HOST/PORT/NAME/USER/PASSWORD

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

接口说明：

```text
POST /token                登录获取 Token（用户名/密码）
POST /system/user_info     获取用户信息
POST /system/logout        注销
GET/POST /system/test      测试表 列表/新增
GET/PUT/DELETE /system/test/{id}   测试表 查询/修改/删除
```

远端环境配置（Python3.6 安装）、Docker 部署 MySQL 5.7、PyCharm 远程开发等详细步骤见教程 `doc/1.md`。

PyCharm 远程开发配置（ssh interpreter）：

![DEMO](doc/images/1-1.png)

## 🔗 相关项目

- 前端：<https://github.com/hequan2017/panda>

## 📄 许可证

[MIT](LICENSE)

## 作者

- 何全，github地址: <https://github.com/hequan2017> ，QQ交流群: 620176501
