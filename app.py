# 网页逻辑交互
import hashlib
import os
import time

from flask import Flask, render_template, request, session, url_for, redirect, send_from_directory

from record_upload_history import append_history, remove_history, list_history
from users_manager import search_user

app = Flask(__name__)
MAX_LIMIT_FILE_SIZE = 64 * 1024 * 1024  # 文件上传尺寸最大限制为64MB
ALLOW_UPLOAD_EXTENSION = ['zip', 'rar', 'jpeg', 'jpg', 'png', 'bmp', 'gif', 'txt']  # 允许的上传格式


class File:  # 文件记录的数据结构,供索引列表使用
    def __init__(self, code: str = None, url: str = None, file_time: str = None, file_name: str = None):
        self.code = code
        self.url = url
        self.file_time = file_time
        self.file_name = file_name

    def get_file_information(self) -> tuple[str, str, str, str]:
        return self.code, self.url, self.file_time, self.file_name


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get("identity") is None:
            return render_template("verity.html")
        else:
            return redirect(url_for("index"))

    code = request.form.get("code")
    password = request.form.get("password")
    if search_user(code, password)[0]:
        session['code'] = code
        session['identity'] = get_hash(code)
        return redirect(url_for("index"))
    return {"状态": "失败", "信息": "Who are you?"}


@app.route("/", methods=['GET', 'POST'])
def index():
    if session.get("identity") is None:
        return redirect(url_for("login"))
    if not os.path.exists('repo'):  # 不存在路径
        os.makedirs('repo')
    file_list = []

    if request.method == 'POST':
        if request.form.get("code").strip() == "":
            return redirect(url_for("index"))

        for history in list_history()['data']:
            if request.form.get("code") == history['code']:
                file_list.append(File(history['code'], history['url'], history['time'], history['url'].split('/')[-1]))
        return render_template("index.html", file_list=file_list, code=session.get("code"))

    for history in list_history()['data']:
        file_list.append(File(history['code'], history['url'], history['time'], history['url'].split('/')[-1]))
    return render_template("index.html", file_list=file_list, code=session.get("code"))


@app.route("/upload", methods=['POST'])
def upload():
    if session.get("identity") is None:
        return redirect(url_for("login"))

    f_list = request.files.getlist('file')
    for f in f_list:
        file_size = len(f.read())
        if file_size <= MAX_LIMIT_FILE_SIZE:
            if f.filename.split('.')[-1].lower() not in ALLOW_UPLOAD_EXTENSION:
                return {"状态": "失败", "信息": "未被允许的文件扩展名,为了主机稳定安全,仅支持以下文件后缀:%s" % ALLOW_UPLOAD_EXTENSION}

            if not os.path.exists('repo/' + session.get("identity")):  # 不存在路径
                os.makedirs('repo/' + session.get("identity"))

            if f.filename in os.listdir('repo/' + session.get("identity")):  # 遇到名字相同的文件,删除之前的文件,简言之就是覆盖
                del_files('repo/' + session.get("identity") + '/' + f.filename)
                remove_history(session.get("code"), 'repo/' + session.get("identity") + '/' + f.filename)

            f.seek(0)  # 文件指针还原
            f.save('repo/' + session.get("identity") + '/' + f.filename)
            append_history(session.get("code"), 'repo/' + session.get("identity") + '/' + f.filename,
                           time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time())))
            return {"状态": "成功", "信息": "文件上传成功"}
        else:
            return {"状态": "失败", "信息": "文件太大了,我的评价是压缩到64MB之内再上传"}


@app.route('/repo/<path:directory>/<filename>')
def download(directory, filename):
    return send_from_directory('repo/' + directory, filename)


@app.route('/delete/repo/<path:directory>/<filename>')
def delete(directory, filename):
    if session.get("identity") != directory:
        return {"状态": "失败", "信息": "Who are you?"}
    else:
        del_files('repo/' + session.get("identity") + '/' + filename)
        remove_history(session.get("code"), 'repo/' + session.get("identity") + '/' + filename)
        return {"状态": "成功", "信息": "目标文件已在主机上移除成功!"}


@app.errorhandler(404)
def error_404(error):
    return {"状态": "404", "信息": "严重怀疑你是不是在搞测试,不然,真的很难出现这个错误"}, 404


@app.route("/feign")
def feign():
    return redirect("")


def del_files(dir_path: str) -> None:
    if os.path.isfile(dir_path):
        os.remove(dir_path)
    elif os.path.isdir(dir_path):
        for file_name in os.listdir(dir_path):
            temp_path = os.path.join(dir_path, file_name)
            del_files(temp_path)


def get_hash(content: str) -> str:
    return hashlib.md5(content.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.config["SECRET_KEY"] = "secret"
    app.run(host='0.0.0.0', port=80, debug=True)
