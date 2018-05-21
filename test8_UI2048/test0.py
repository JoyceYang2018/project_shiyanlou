#coding:utf-8

import wx

#每个wxPython的程序都要有一个wx.App对象
app = wx.App()


"""
None:当前窗口的父窗口parent，如果当前窗口是最顶层，则parent=None，如果不是顶层窗口，则它的值为所属frame的名字
-1:id值，-1的话程序会自动产生一个id
pos:位置
size:宽，高，大小
还有风格参数style，不填默认市这样几个组合
wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX
可以去掉几个看看效果
style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX

"""

frame = wx.Frame(None,-1,title='wx_00_base.py',pos=(300,400),size=(200,150))#,style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)

frame.Show()

app.MainLoop()