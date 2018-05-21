#coding:utf-8

#对不同的文件块进行分类处理


class Handler:
    #处理程序的父类
    def callback(self,prefix,name,*args):
        method = getattr(self,prefix+name,None)
        #先获取self.prefix+name这个方法，如果没有，method为None
        if callable(method):
            return method(*args)
        #如果这个方法有且可以调用，返回self.prefix+name(),即调用

    def start(self,name):
        self.callback('start_',name)

    def end(self,name):
        self.callback('end_',name)

    def sub(self,name):
        def substitution(match):
            result = self.callback('sub_',name,match)
            if result is None:
                result = match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):
    #HTML处理程序，给文本块对应位置加相应的HTML标记
    def start_document(self):
        print('<html><head><title>Joyce</title></head><body>')

    def end_document(self):
        print('</body></html>')

    def start_paragraph(self):
        print('<p style="color: #444;">')

    def end_paragraph(self):
        print('</p>')

    def start_heading(self):
        print('<h2 style="color:#68BE5D;">')

    def end_heading(self):
        print('</h2>')

    def start_list(self):
        print('<ul style="color: #363736;">')

    def end_list(self):
        print('</ul>')

    def start_listitem(self):
        print('<li>')

    def end_listitem(self):
        print('</li>')

    def start_title(self):
        print('<h1 style="color: #1ABC9C;">')

    def end_title(self):
        print('</h1>')

    def sub_emphasis(self,match):
        return '<em>%s</em>'%match.group(1)

    def sub_url(self,match):
        #a标签转向的页面在新打开的未命名窗口载入 _blank
        return '<a target="_blank" style="text-decoration:none;color:#BC1A4B;" href="%s">%s</a>'%(match.group(1),match.group(1))

    def sub_mail(self,match):
        return '<a style="text_decoration:none;color:#BC1A4B;" href="mailto:%s">%s</a>'%(match.group(1),match.group(1))

    def feed(self,data):
        print(data)