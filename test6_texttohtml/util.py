#coding:utf-8

#对文件进行分块处理，并返回生成器




def lines(file):
    #把txt文件变成生成器，并在文本最后家一空行
    for line in file:
        yield line
    yield '\n'


def blocks(file):
    #生成器，把文本分割成单独的文本快
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block=[]