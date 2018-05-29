#coding:utf-8

import sys,os,BaseHTTPServer,subprocess

class ServerException(Exception):
    #服务器内部错误
    pass


class case_no_file(object):
    #路径不存在
    def test(self,handler):
        return not os.path.exists(handler.full_path)

    def act(self,handler):
        raise ServerException("'{0}' not found".format(handler.path))




class case_existing_file(object):
    # 路径是文件
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        handler.handle_file(handler.full_path)


class case_always_fail(object):
    # 所有情况都不符合时的默认处理类
    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))




class case_directory_index_file(object):
    # 主页路径
    def index_path(self,handler):
        return os.path.join(handler.full_path,'index_self.html')

    #判断目标路径是否是目录&&目录下是否有index.html
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    #响应index.html的内容
    def act(self, handler):
        handler.handle_file(self.index_path(handler))



class case_cgi_file(object):
    #脚本文件处理
    def test(self,handler):
        return os.path.isfile(handler.full_path) and \
               handler.full_path.endswith('.py')

    def act(self,handler):
        #运行脚本文件
        handler.run_cgi(handler.full_path)



class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    请求路径合法则返回相应处理
    否则返回错误页面
    '''

    Cases =[
        case_no_file(),
        case_cgi_file(),
        case_existing_file(),
        case_directory_index_file(),
        case_always_fail()
    ]

    #错误页面模板
    Error_Page = '''\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
    '''

    def do_GET(self):
        try:
            # 文件完整路径,os.getcwd()是当前工作目录，self.path保存了请求的相对路径
            self.full_path = os.getcwd() + self.path

            # 遍历所有的情况并处理
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break

        # 处理异常
        except Exception as msg:
            self.handle_error(msg)


    def run_cgi(self,full_path):
        data = subprocess.check_output(["python",self.full_path])
        self.send_content(data)



    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)



    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

    def send_content(self, page, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)



if __name__ == '__main__':
    serverAddress = ('',8080)
    server = BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()