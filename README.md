# EFO: Earth Four-body Organization
其实嘛。。。这个项目叫 ~~ 红糖大米粥论坛？！ ~~

[前端文件](https://github.com/dmzhtj/EFO-Front-End)在[dmz](https://github.com/dmzhtj)那里。~~ 放了就能用 ~~

代码构建环境：
1. Linux Mint Zara(22.2)|Linux 6.8.0-90-generic x86_64 GNU/Linux
2. Python 3.12.3 (apt package,ubuntu noble) virtualenv 20.25.0+ds
3. (网络测试) OpenWrt 25.12.4 r32933-4ccb782af7 / LuCI branch 26.bcm27xx/bcm2711 Firmware:133.20346~e9ebca7 Kernel:6.12.87

部署先在venv中运行 `init.sh`，修改 `settings.py`，然后按照flask服务正常部署（Gunicorn/uWSGI）。WSGI入口使用 `main:disp.app`，导入 `main` 不会启动 Flask 开发服务器。测试请使用 `python3 main.py`。

### License
User agreement is set by [dmz](https://github.com/dmzhtj)(see `LICENSE-EFO`).

The project is under MIT License(see `LICENSE`).
