from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class MainWindow(QMainWindow):

    #自定义信号
    my_signal = pyqtSignal(str)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #设置窗口标题
        self.setWindowTitle('My First App')

        button = QPushButton('Click me!')
        button.pressed.connect(self._click_button)
        #将自定义信号与相应的槽函数连接
        self.my_signal.connect(self._my_func)
        #将部件添加到主窗口上
        self.setCentralWidget(button)


    #自定义的信号处理函数
    def _click_button(self):
        #当按钮被点击的时候发出信号 my_signal
        self.my_signal.emit('shiyanlou')

    def _my_func(self,s):
        print(s)

# 创建应用实例，通过 sys.argv 传入命令行参数
app = QApplication(sys.argv)
# 创建窗口实例
window = MainWindow()
# 显示窗口
window.show()
# 执行应用，进入事件循环
app.exec_()