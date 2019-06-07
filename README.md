# py4S

py4S 是 py Simple Shadowsocks Subscribe Server 的缩写，一个使用 Sanic 开发的简易订阅服务。

[瓦工机场 GIA-E 线路](https://justmysocks1.net/members/aff.php?aff=1025) 

注：链接有 aff code

## 如何使用

推荐使用 Docker 运行。

### 配置

使用 `subscribe.toml` `config.toml` 作为配置文件。

* subscribe.toml

用于保存订阅内容配置

```toml
[[subscribe]]
uid="82bce78f-a084-48ac-9cbf-47693e0d0945"
token="9c96af410fd36031"
[[subscribe.shadowsocks]]
server="111.111.111.111"
server_port=11111
password="111password"
method="aes-256-gcm"
remark="BWG-US-CA"
[[subscribe.shadowsocks]]
server="222.222.222.222"
server_port=22222
password="222password"
method="aes-256-gcm"
remark="BWG-US-AZ"

[[subscribe]]
uid="2d0c75c8-4e9a-41ab-8584-a19ddfd9586f"
token="49c1d89cba81644e"
[[subscribe.shadowsocks]]
server="111.111.111.111"
server_port=11111
password="111password"
method="aes-256-gcm"
remark="BWG-US-CA"
[[subscribe.shadowsocks]]
server="222.222.222.222"
server_port=22222
password="222password"
method="aes-256-gcm"
remark="BWG-US-AZ"
```

* `config.toml`

用于保存服务配置，目前没任何用处,但必须存在。


### 部署

1. 安装 Docker 与 docker-compose

1. 创建目录 `py4s/config` 并创建 `config.toml` 与 `subscribe.toml`

1. 创建 `py4s/docker-compose.yaml`

    ```yaml
    version: "3"
    services:
     py4s:
      image: tomczhen/py4s
      restart: unless-stopped
      ports:
        - 8000:8000
      volumes:
        - ./config:/app/config
    ```

1. 在 `py4s` 目录下执行 `docker-compose up -d`

1. 使用 `docker-compose logs` 查看日志

## 获取订阅

通过 `http://0.0.0.0:8000/subscribe/{uid}?token={token}` 获取订阅信息。

注意：如果请求 `accept-content` 头中有 `text/html` 则无法获取订阅。