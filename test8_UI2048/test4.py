#coding:utf-8

import wx
from math import *

class CalcFrame(wx.Frame):

    def __init__(self,title):
        super(CalcFrame, self).__init__(None,title=title,size = (300,250))

        self.InitUI()
        self.Centre()
        self.Show()


    def InitUI(self):
        #定义计算器初始UI
        vbox = wx.BoxSizer(wx.VERTICAL)
        #BoxSizer可以行列放置控件，先放文本框
        self.textprint = wx.TextCtrl(self,-1,'',style=wx.TE_RIGHT|wx.TE_READONLY)
        #设置文本框只可以计算器上的数字被输入，而不希望键盘输入
        self.equation = ''
        #用来储存textprint的内容，方便之后调用
        vbox.Add(self.textprint,flag = wx.EXPAND|wx.TOP|wx.BOTTOM,border = 4)

        #用GridSizer放置按钮
        gridbox=wx.GridSizer(5,4,5,5)
        #四个参数分别为行数，列数，格子之间垂直间隔，格子之间水平间隔
        labels = ['AC','DEL','pi','CLOSE','7','8','9','/','4','5','6','*','1','2','3','-','0','.','=','+']
        for label in labels:
            buttomitem = wx.Button(self,label=label)
            self.createHandler(buttomitem,label)
            gridbox.Add(buttomitem,1,wx.EXPAND)
        vbox.Add(gridbox,proportion=1,flag=wx.EXPAND)
        self.SetSizer(vbox)


    def createHandler(self,button,labels):
        item='DEL AC = CLOSE'
        if labels not in item:
            self.Bind(wx.EVT_BUTTON,self.OnAppend,button)
        elif labels =='DEL':
            self.Bind(wx.EVT_BUTTON,self.OnDel,button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON, self.OnAc, button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON, self.OnTarget, button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON, self.OnExit, button)



    def OnAppend(self,event):
        eventbutton = event.GetEventObject()
        label = eventbutton.GetLabel()
        self.equation+=label
        self.textprint.SetValue(self.equation)

    def OnDel(self,event):
        self.equation=self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def OnAc(self,event):
        self.textprint.Clear()
        self.equation=""
        
    def OnTarget(self,event):
        string = self.equation
        try:
            target = eval(string)
            self.equation = str(target)
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            dlg = wx.MessageDialog(self,u'格式错误，请输入正确的等式！',u'请注意',wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnExit(self,event):
        self.Close()


if __name__ == '__main__':

    app = wx.App()
    CalcFrame(title='Calculator')
    app.MainLoop()

