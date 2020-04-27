1.在树莓派系统上执行一下命令
创建文件名为 ``install_adb.sh``,并赋予权限为 ``chmod +x install_adb.sh``
```
#!/usr/bin/env bash
yes|apt-get update
yes|apt-get install adb
yes|apt-get install supervisor
systemctl enable supervisor
systemctl start supervisor
```

2.把可用的程序放在 ``/usr/local/pay_client``下，只需要把src同级别的文件放在次目录下即可，
pay_client 为发布目录

3.配置 supervisor
```
apt-get install supervisor
systemctl enable supervisor
systemctl start supervisor
```

设置 pay_client的自动启动，进入到``/etc/supervisor/conf.d`` 目录下增加如下配置，并起名为
``pay_client.conf``

```
[program:app]
command =python3 /user/local/pay_client/run.py -log=stdout
;注意这里只能为1
numprocs = 1
autostart = true
autorestart = true
;以下为日志,按实际情况修改
stdout_logfile = /var/log/supervisor/app.log
stdout_logfile_maxbytes = 50MB
stderr_logfile = /var/log/supervisor/app_error.log
stderr_logfile_maxbytes = 50MB
```

增加完毕后通过命令``systemctl restart supervisor``来重启，将自动开始工作
使用命令``supervisorctl status`` 查看 ``app`` 的运行情况如果失败找到元婴并进行重启
即可，一般经过以上步骤都将正常启动

4.进行关机，并重新启动尝试，查看``app`` 是否自动随着开机而启动，并工作

5.配置树莓派的wifi连接（如果可以线连接尽量线，wifi同时连接避免有一个不可用导致无法上网）
打开文件``/etc/wpa_supplicant/wpa_supplicant.conf``

```
network={
	ssid="账户"
	psk="密码"
	key_mgmt=WPA-PSK
}
```

其中``key_mgmt=WPA-PSK``默认即可，大部分默认可以，如果重启发现无法连接网络就需要修改或者注释掉

6.配置完毕后可以针对具体的场景上写image镜像文件，需要是直接复制克隆修改数据即可


7. 启动 uiautomator2 的后台进程
参考链接https://github.com/openatx/uiautomator2#selector
python3 -m uiautomator2 init

启动调试 web界面，图形化可视
weditor