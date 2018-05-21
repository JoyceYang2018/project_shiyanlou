#coding:utf-8

#文件块处理规则


class Rule:
    #定义规则的父类
    def action(self,block,handler):
        #加标记
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        #注意：这几个方法在handlers中定义的时候被调用直接print内容，所以直接返回就可以了
        return True

class HeadingRule(Rule):
    #一号标题规则
    type='heading'
    def condition(self,block):
        #判断是否符合规则
        return not '\n' in block and len(block)<=70 and not block[-1]==':'

class TitleRule(HeadingRule):
    #二号标题规则,如果标题第一次出现则为二号标题，之后再也不视为二号标题
    type = 'title'
    first = True

    def condition(self,block):
        if not self.first:
            return False
        self.first=False
        return HeadingRule.condition(self,block)

class ListItemRule(Rule):
    #列表项规则
    type='listitem'
    def condition(self,block):
        return block[0]=='-'

    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    #列表规则
    type='list'
    inside = False
    def condition(self,block):
        return True
    def action(self,block,handler):
        if not self.inside and ListItemRule.condition(self,block):
            #判断如果不在列表内部且出现'-'则列表开始
            handler.start(self.type)
            self.inside=True
        elif self.inside and not ListItemRule.condition(self,block):
            #判断如果在列表内部切没有'-'，则列表结束
            handler.end(self.type)
            self.inside=False
        return False


class ParagraphRule(Rule):
    #段落规则
    type='paragraph'

    def condition(self,block):
        return True

