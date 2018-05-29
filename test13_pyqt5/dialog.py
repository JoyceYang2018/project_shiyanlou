from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

#自定义对话框
class CustomDialog(QDialog):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowTitle('New Dialog')
        #添加按钮选项
        QBtn= QDialogButtonBox.Ok|QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(buttonBox)
        self.setLayout(layout)



class MainWindow(QMainWindow):


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #设置窗口标题
        self.setWindowTitle('My First App')

        #设置标签
        label = QLabel('Welcome to Shiyanlou!')
        #设置标签显示在中央
        label.setAlignment(Qt.AlignCenter)
        #添加标签到主窗口
        self.setCentralWidget(label)



        #添加按钮动作，并加载图标图像
        button_action = QAction('New Dialog',self)
        button_action.triggered.connect(self.onButtonClick)



        #添加菜单栏
        mb = self.menuBar()
        #禁用原生的菜单栏
        mb.setNativeMenuBar(False)
        #添加“文件”菜单
        file_menu = mb.addMenu('&File')
        #为文件菜单添加动作
        file_menu.addAction(button_action)



    def onButtonClick(self,s):
        #创建对话框
        dlg = CustomDialog(self)
        #运行对话框,这步非常重要！！！！！！！
        dlg.exec_()







# 创建应用实例，通过 sys.argv 传入命令行参数
app = QApplication(sys.argv)
# 创建窗口实例
window = MainWindow()
# 显示窗口
window.show()
# 执行应用，进入事件循环
app.exec_()


