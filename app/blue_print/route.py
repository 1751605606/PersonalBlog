# 导入蓝本 blue_print
from . import blue_print
from flask import *
import json
from app.models import *
from app import db


@blue_print.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@blue_print.route('/api/user/register', methods=['GET','POST'])
def user_register():
    if request.method == 'POST':
        json_data = json.loads(request.get_data())
        username = json_data.get("username")
        password = json_data.get("password")
        user = db.session.query(User).filter(User.username == username).first()
        # 用户名未被使用
        if user is None:
            user = User(username, password, 0)
            try:
                user.add_user()
            # 发生异常
            except Exception as e:
                return {
                    "code": "200",
                    "error": {
                        "type": "exception occur",
                        "message": str(e)
                    },
                    "data": {}
                }
            # 未发生异常
            else:
                return {
                    "code": "200",
                    "error": {},
                    "data": {
                        "token": "token"
                    }
                }
        else:
            return {
                "code": "200",
                "error": {
                    "type": "username repeat",
                    "message": username + " has been used"
                },
                "data": {}
            }
    return render_template("register.html")

#  #单用户版本
# @blue_print.route('/api/user/login_1', methods=['POST', 'GET'])
# def user_login_1():
#     if request.method == 'POST':
#         json_data = json.loads(request.get_data())
#         username = json_data.get("username")
#         password = json_data.get("password")
#         if username == 'admin' and password == 'admin':
#             session['username'] = username
#             return {
#                 "code": "200",
#                 "error": {},
#                 "data": {
#                     "token": "token"
#                 }
#             }
#         else:
#             return {
#                 "code": "200",
#                 "error": {
#                     "type": "user not found",
#                     "message": "no such user: " + username
#                 },
#                 "data": {}
#             }
#     if 'username' in session:
#         return {
#                 "code": "200",
#                 "error": {},
#                 "data": {
#                     "token": "token"
#                 }
#             }
#     return render_template("login.html")


# 多用户版本

@blue_print.route('/api/user/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        json_data = json.loads(request.get_data())
        username = json_data.get("username")
        password = json_data.get("password")
        user = db.session.query(User).filter_by(username=username, password=password).first()
        if user is None:
            return {
                "code": "200",
                "error": {
                    "type": "user not found",
                    "message": "username or password is not right"
                },
                "data": {}
            }
        else:
            session['username'] = username
            group_id = "1" if username == 'admin' else "0"
            return {
                "code": "200",
                "error": {},
                "data": {
                    "id": user.id,
                    "group_id": group_id,
                    "token": "token"
                }
            }
    if 'username' in session:
        return {
                "code": "200",
                "error": {},
                "data": {
                    "token": "token"
                }
            }
    return render_template("login.html")


@blue_print.route('/api/user/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('user_login'))


