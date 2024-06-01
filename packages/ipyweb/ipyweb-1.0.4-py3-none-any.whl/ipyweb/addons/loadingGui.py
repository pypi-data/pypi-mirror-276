import urllib.parse
from ipyweb.logger import logger
from ipyweb.singleton import singleton
from ipyweb.utils import utils


class loadingGui(metaclass=singleton):

    @classmethod
    def redirect(self, winCls=None, url=''):
        if winCls is None or winCls.windows == None or url == '':
            logger.console.error(f'An exception occurred while reloading the window parameters')
        try:
            domain, port = utils.getDomainPortByUrl(urllib.parse.quote(url, safe='/:?=&+'))
            if utils.checkUrl(domain, port) == True:
                winCls.windows.load_url(url)
            else:
                winCls.windows.load_html(self.html(f'网络异常无法加载请重试'))
        except Exception as e:
            winCls.windows.load_html(self.html(f'加载窗口地址异常请关闭重新打开再试'))
            logger.console.error(f'An exception occurred while reloading the window url: {e}')

    @classmethod
    def load(self, winCls=None):
        try:
            if winCls:
                winCls.setCreateParams({'html': self.html('正在加载中...')})
        except Exception as e:
            logger.console.error(f'An exception occurred while reading the login page: {e}')

    @classmethod
    def html(self, message='正在加载中...'):
        return """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0, minimum-scale=1.0" /><title></title>
 <style>html body{ overflow: hidden;}
      #loadingPage {background-color: #dedede;font-size: 12px;cursor: pointer;}
       #message{position: absolute;bottom:10px;width:100%;height:30px;line-height:30px;font-size:12px; text-align: center; color:#aaa; overflow: hidden;}
      .base {height: 9em;left: 50%;margin: -7.5em;padding: 3em;position: absolute;top: 50%; width: 9em;transform: rotateX(45deg) rotateZ(45deg);transform-style: preserve-3d;}
      .cube,
      .cube:after,
      .cube:before {content: ''; float: left;height: 3em; position: absolute;width: 3em;}
      .cube {background-color: #06cf68;position: relative;transform: translateZ(3em);transform-style: preserve-3d;transition: .25s;box-shadow: 13em 13em 1.5em rgba(0, 0, 0, 0.1);animation: anim 1s infinite;}
      .cube:after {background-color: #05a151;transform: rotateX(-90deg) translateY(3em);transform-origin: 100% 100%;}
      .cube:before {background-color: #026934; transform: rotateY(90deg) translateX(3em);transform-origin: 100% 0;}
      .cube:nth-child(1) { animation-delay: 0.05s;}
      .cube:nth-child(2) {animation-delay: 0.1s;}
      .cube:nth-child(3) {animation-delay: 0.15s;}
      .cube:nth-child(4) {animation-delay: 0.2s;}
      .cube:nth-child(5) {animation-delay: 0.25s;}
      .cube:nth-child(6) {animation-delay: 0.3s;}
      .cube:nth-child(7) {animation-delay: 0.35s;}
      .cube:nth-child(8) {animation-delay: 0.4s;}
      .cube:nth-child(9) {animation-delay: 0.45s;}
      @keyframes anim {50% {transform: translateZ(0.5em)}}
    </style>
  </head>
  <body>
    <div id="loadingPage"><div class='base'><div class='cube'></div><div class='cube'></div><div class='cube'></div><div class='cube'></div><div class='cube'></div><div class='cube'></div><div class='cube'></div><div class='cube'></div><div class='cube'></div></div></div>
    <div id="message">
    """ + message + """    
    </div>
  </body>
</html>

            """
