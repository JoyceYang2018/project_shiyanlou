from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys

class MainWindoow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #设置窗口标题
        self.setWindowTitle('My Browser')
        #设置窗口图标
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.show()


        #添加标签栏
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        #允许关闭标签
        self.tabs.setTabsClosable(True)
        #设置关闭按钮的槽
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.add_new_tab(QUrl('http://shiyanlou.com'),'Homepage')
        self.setCentralWidget(self.tabs)

        new_tab_action=QAction("icons/add_page.png",'New Page',self)
        new_tab_action.triggered.connect(self.add_new_tab)



        #添加导航栏
        navigation_bar = QToolBar('Navigation')
        #设定图标大小
        navigation_bar.setIconSize(QSize(16,16))
        self.addToolBar(navigation_bar)

        #添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/back.png'),'Back',self)
        next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)

        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)

        #将按钮添加到导航栏
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)



        #添加url地址
        self.urlbar = QLineEdit()
        #让地址栏可以响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)


    def renew_urlbar(self,q,browser=None):
        #如果不是当前窗口所展示的网页则不更新url
        if browser != self.tabs.currentWidget():
            return
        #将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


    #响应回车按钮，将浏览器当前访问的url设置为用户输入的url
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme()=='':
            q.setScheme('http')
        self.browser.setUrl(q)

    #添加新的标签页
    def add_new_tab(self,qurl=QUrl(''),label='Blank'):
        # 为标签创建新网页
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # 为标签页添加索引方便管理
        i=self.tabs.addTab(browser,label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl,browser=browser:self.renew_urlbar(qurl,browser))

        # 加载完成之后将标签标题修改为网页相关的标题
        browser.loadFinished.connect(lambda _,i=i,browser = browser:
                                     self.tabs.setTabText(i,browser.page().mainFrame().title()))

    #双击标签栏打开新页面
    def tab_open_doubleclick(self,i):
        if i==-1:
            self.add_new_tab()


    def current_tab_changed(self,i):
        qurl = self.tabs.currentWidget().url()
        self.renew_urlbar(qurl,self.tabs.currentWidget())


    def close_current_tab(self,i):
        #如果当前标签页只剩下一个则不关闭
        if self.tabs.count()<2:
            return
        self.tabs.removeTab(i)



#创建应用
app = QApplication(sys.argv)
#创建主窗口
window = MainWindoow()
#显示窗口
window.show()
#运行应用，并监听事件
app.exec_()