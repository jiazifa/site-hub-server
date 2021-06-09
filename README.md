# site-hub-server

## 介绍

本项目是 site-hub 的后端服务

构建的主要目的是提供一个站点收集的工具

也许之后会添加一些其他的内容

目前是作为 site-hub 的后端服务

涉及仓库：

> site-hub-web 前端
>
> ToolHUB 目前负责补充数据


## 安装

使用 poetry

    如果你安装了 poetry ,推荐你使用 `./scripts/initialize.sh` 来安装以及初始化项目


使用 pip

    运行 `pip install -r requirements.txt` 命令可以安装项目依赖


## 配置文件

你需要在项目根目录创建一个 `local_settings.py` 的配置文件

你可以通过覆盖项目默认的选项，达到自定义配置的目的

这些配置项通常可以在 `app/config.py` 文件中找到


## 运行

`poetry run python runner.py` 或其他方式

## 问题

- AttributeError: can't set attribute 

有时候数据库有问题，会有这种情况

## 目前功能

- [x] 每日一句 (通过ToolHUB仓库补充数据) 

- [x] 站点的增删改查

## Todo

- [ ] 添加的站点可以获得站点的截图显示

- [ ] 用户模块

- [ ] 其他...

## 其他 

如果你有任何想法或者建议，都可以通过 issue 或邮件联系我