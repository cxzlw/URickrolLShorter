import random

from flask import Flask, render_template, request, redirect, url_for
import flask
import sqlobject as sql
from sqlobject.sqlite import builder

app = Flask(__name__)

DBNAME = 'data.db'
db = builder()(DBNAME)


class Short(sql.SQLObject):
    class sqlmeta:
        table = "short"

    _connection = db
    long = sql.StringCol()
    short = sql.StringCol()


def randomstr():
    length = random.randint(5, 8)
    string = ""
    choices = "1qaz2wsx3edc4rfv5tgbnhy67ujmki89olp0"
    for x in range(length):
        string += random.choice(choices)
    return string


@app.route('/', methods=['GET', 'POST'])  # 注册
def register():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        long = 'long' in request.form and request.form['long']
        if long:
            selected = Short.select(Short.q.long == long)
            if selected.count() == 0:
                short = randomstr()
                while Short.select(Short.q.short == short).count() != 0:
                    short = randomstr()
                s = Short(long=long, short=short)
                return render_template('tips.html', tip_text=f"您的短链接是url://s/{s.short}",
                                       buttons=[{"text": "继续生成", "url": "/"}])
            else:
                return render_template('tips.html', tip_text=f"您的短链接是url://s/{selected[0].short}",
                                       buttons=[{"text": "继续生成", "url": "/"}])

        else:
            return render_template('tips.html', tip_text="您提交的信息不全，请将信息填写完整",
                                   buttons=[{"text": "重新生成", "url": "/"}])


@app.route("/s/<short>")
def short_normal(short):
    selected = Short.select(Short.q.short == short)
    if selected.count() != 0:
        return render_template("iframe.html", url=selected[0].long)
    else:
        return render_template("404.html"), 404


@app.route("/<path:p>")
def an(p):
    return redirect("https://vdse.bdstatic.com//192d9a98d782d9c74c96f09db9378d93.mp4")


@app.errorhandler(404)  # 404找不到网页错误
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)  # 500服务器内部程序错误
def error(e):
    return render_template('500.html'), 500


def init_db():
    Short.createTable(ifNotExists=True)
    print('数据库初始化完成!')


init_db()

if __name__ == '__main__':
    app.run("0.0.0.0", port=80)
