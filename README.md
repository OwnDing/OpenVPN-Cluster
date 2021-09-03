# OpenVPN-Cluster
# OpenVPN 集群
最近在准备OpenVPN的集群供IoT设备使用，参考了
- https://github.com/BrunoTh/OpenVPN-Cluster
- https://github.com/kylemanna/docker-openvpn

## 说明
由于 [Bruno](https://github.com/BrunoTh/OpenVPN-Cluster) 提供的Dcokerfile是两年前的，导致build镜像时出现了很多问题，现提供修改后的Dcokerfile文件。\
本次测试采用的是CentOS 7.6 系统。\
主网卡 eth0。

## 步骤
- 使用 [kylemanna/openvpn](https://hub.docker.com/r/kylemanna/openvpn/) 镜像初始化证书，并生成两个用户文件：user1、user2
- 启动两个新打包的openvpn容器
- 在 ccd 文件夹中新增两个 user1、user2文件，配置不同的静态IP：192.168.255.6；192.168.255.10
![静态IP](https://github.com/OwnDing/OpenVPN-Cluster/blob/main/pic/sip.PNG)

- 使用两个客户端连接到不同的openvpn容器，会发现python脚本会自动添加相关的路由信息
![路由](https://github.com/OwnDing/OpenVPN-Cluster/blob/main/pic/route.PNG)

- 在客户端中 ping 另一个vpn的静态IP
![Ping](https://github.com/OwnDing/OpenVPN-Cluster/blob/main/pic/ping.PNG)
