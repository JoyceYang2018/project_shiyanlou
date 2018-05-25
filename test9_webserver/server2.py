#coding:utf-8

import sys,os,BaseHTTPServer

class ServerException(Exception):
    #服务器内部错误
    pass




class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            #文件完整路径,os.getcwd()是当前工作目录，self.path保存了请求的相对路径
            full_path = os.getcwd()+self.path

            #如果该路径不存在
            if not os.path.exists(full_path):
                #抛出异常：文件未找到
                raise ServerException("'{0}' not found".format(self.path))

            #如果该路径是一个文件
            elif os.path.isfile(full_path):
                #调用 handler_file处理该文件
                self.handle_file(full_path)

            #如果该路径不是一个文件
            else:
                #抛出异常：该路径为不知名对象
                raise ServerException("Unknown object '{0}'".format(self.path))


        #处理异常
        except Exception as msg:
            self.handle_error(msg)



    def handle_file(self,full_path):
        try:
            with open(full_path,'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg="'{0}' cannot be read: {1}".format(self.path,msg)
            self.handle_error(msg)


    Error_Page = '''\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
    '''


    def handle_error(self,msg):
        content = self.Error_Page.format(path = self.path,msg = msg)
        self.send_content(content,400)



    def send_content(self,page,status=200):
        self.send_response(status)
        self.send_header("Content-Type","text/html")
        self.send_header("Content-Length",str(len(page)))
        self.end_headers()
        self.wfile.write(page)
        pass




if __name__ == '__main__':
    serverAddress = ('',8080)
    server = BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()

