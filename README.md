# site-hub-server

site-hub 的后端服务

- 涉及仓库：

> site-hub-web 前端
> ToolHUB 目前负责补充数据


### 介绍

本项目是 site-hub 的后端服务


### 安装


##### 安装依赖
 
**Linux**

安装docker

`curl -sSL https://get.daocloud.io/docker | sh`


安装poetry

`pip install poetry docker-compose`


项目初始化， 目前仅适用于首次
`./scripts/initialize.sh`


###### 运行

`poetry run python runner.py` 或其他方式

**Docker部署**

`docker-compose up`