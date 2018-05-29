from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys


#用于显示色块
class Color(QWidget):
    def __init__(self,color,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window,QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #设置窗口标题
        self.setWindowTitle('My First App')

        colors =['red','green','blue','yellow']

        # #水平布局
        # #layout = QVBoxLayout()
        # #垂直布局
        # layout = QHBoxLayout()
        #
        # for color in colors:
        #     layout.addWidget(Color(color))

        #网格布局
        layout = QGridLayout()

        for i,color in enumerate(colors):
            for j in range(len(colors)):
                layout.addWidget(Color(color),i,j)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)



# 创建应用实例，通过 sys.argv 传入命令行参数
app = QApplication(sys.argv)
# 创建窗口实例
window = MainWindow()
# 显示窗口
window.show()
# 执行应用，进入事件循环
app.exec_()