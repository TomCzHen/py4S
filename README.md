# py4S

py4S 是 py Simpale Shadowsocks Subscribe Server 的缩写，一个使用 Sanic 开发的简易订阅服务。

[瓦工机场 GIA-E 线路](https://justmysocks1.net/members/aff.php?aff=1025) 

注：链接有 aff code

## How to use

使用 `shadowsocks.toml` 作为配置文件。

```toml
[82bce78f-a084-48ac-9cbf-47693e0d0945] # subscribe id
uid="82bce78f-a084-48ac-9cbf-47693e0d0945"
token="9c96af410fd36031"
[[82bce78f-a084-48ac-9cbf-47693e0d0945.shadowsocks]]
server="111.111.111.111"
server_port=11111
password="111password"
method="aes-256-gcm"
remark="example-server-1"
[[82bce78f-a084-48ac-9cbf-47693e0d0945.shadowsocks]]
server="222.222.222.222"
server_port=22222
password="222password"
method="aes-256-gcm"
remark="example-server-2"
```

参考示例文件配置好订阅内容后保存为 `shadowsocks.toml`。

```bash
docker-compose up -d
```

即可通过 `http://0.0.0.0:8000/subscribe/{uid}?token={token}` 获取订阅信息。

注意：如果请求 `accept-content` 头中有 `text/html` 则无法获取订阅。