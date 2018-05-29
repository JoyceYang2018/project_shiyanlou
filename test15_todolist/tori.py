import pymysql
import argparse
import json
import os

from flask import Flask,g,jsonify,render_template,request,abort

MYSQL_HOST = os.environ.get('MYSQL_HOST') or '127.0.0.1'
MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3306
TODO_DB = 'todoapp'

def dbSetup():
    conn = pymysql.connect(host = MYSQL_HOST,port = MYSQL_PORT,user = 'root',passwd = '123456',db=TODO_DB,charset = 'utf8')
    cursor = conn.cursor()
    sql = "CREATE TABLE if not exists todos(id int auto_increment not null primary key,title varchar(256),done tinyint(1) not null default 0)"
    cursor.execute(sql)
    conn.close()


app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    try:
        g.mysql_conn = pymysql.connect(host = MYSQL_HOST,port = MYSQL_PORT,user = 'root',passwd = '123456',db=TODO_DB,charset = 'utf8')
    except Exception:
        abort(503,"No database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    try:
        g.mysql_conn.close()
    except Exception:
        pass


@app.route("/todos",methods=['GET'])
def get_todos():
    cursor = g.mysql_conn.cursor()
    sql = "SELECT * FROM todos"
    cursor.execute(sql)
    list = ['id','title','done']
    selection = []
    for select in cursor.fetchall():
        selection.append(dict(zip(list,select)))
    return json.dumps(selection)


@app.route("/todos",methods=['POST'])
def new_todo():
    cursor = g.mysql_conn.cursor()
    sql = "insert into todos(title,done) values ('%s','%d')"%(request.json['title'],request.json['done'])
    try:
        cursor.execute(sql)
        g.mysql_conn.commit()
    except:
        g.mysql_conn.rollback()
    return jsonify(id='%d'% (cursor.execute("select id from todos where title='%s'"%(request.json['title']))))


@app.route("/todos/<string:todo_id>",methods = ['GET'])
def get_todo(todo_id):
    cursor = g.mysql_conn.cursor()
    sql = "SELECT * FROM todos where id = '%d'"%(int(todo_id))
    cursor.execute(sql)
    list = ['id', 'title', 'done']
    selection = dict(zip(list, cursor.fetchone))
    return json.dumps(selection)




@app.route("/todos/<string:todo_id>",methods=['PUT'])
def update_todo(todo_id):
    cursor = g.mysql_conn.cursor()
    sql = "update todos set title = '%s',done = '%d' where id = '%d'"%(request.json['title'],request.json['done'],int(todo_id))
    try:
        cursor.execute(sql)
        g.mysql_conn.commit()
    except:
        g.mysql_conn.rollback()
    return json.dumps(cursor.execute(sql))


@app.route("/todos/<string:todo_id>",methods=['DELETE'])
def delete_todo(todo_id):
    cursor = g.mysql_conn.cursor()
    sql = "delete from todos where id = '%d'" %(int(todo_id))
    try:
        cursor.execute(sql)
        g.mysql_conn.commit()
    except:
        g.mysql_conn.rollback()
    return jsonify(cursor.execute(sql))


@app.route("/")
def show_todos():
    return render_template('todo.html')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask todo app')
    parser.add_argument('--setup',dest='run_setup',action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        dbSetup()
    else:
        app.run(debug=True)
