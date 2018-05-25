import  wx


class Example(wx.Frame):
    def __init__(self,title,shapes):
        super(Example, self).__init__(None,title = title,size=(600,400))
        self.shapes = shapes

        self.Bind(wx.EVT_PAINT,self.OnPoint)

        self.Centre()
        self.Show()


    def OnPoint(self,e):
        dc = wx.PaintDC(self)

        for shape in self.shapes:
            dc.SetPen(wx.Pen(shape.color))
            dc.DrawLines(shape.drawPoints())

            