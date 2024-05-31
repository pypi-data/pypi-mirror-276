```bash
pip install -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 使用QT

```bash
pip install pywebview qtpy  pyside2
sudo apt-get install libxcb-xinerama0
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine python3-pyqt5.qtwebchannel libqt5webkit5-dev libxcb-xinerama0
### pip install pyqtwebengine
```

### 使用gtk

```bash
sudo apt-get install cmake python3-dev libcairo2-dev pkg-config build-essential  libgirepository1.0-dev
pip3 install pycairo pygobject 
```

### 注意事项

- 调整pywebview5.1 platform/winforms.py 614 加入cef模式下不创建缓存文件夹问题 加入init_storage()创建缓存文件夹函数
- 'ignore_certificate_errors':true #忽略证书错误
- 'locale': 'zh-CN'
- 开启ssl 需要pip install cryptography