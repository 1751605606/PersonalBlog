# 导入蓝本 blue_print
from . import blue_print
from flask import *
import json
from app.models import *
from app import db
from . import utils


@blue_print.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@blue_print.route('/api/user/register', methods=['GET', 'POST'])
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
                    "code": "502",
                    "error": {
                        "type": "exception occur",
                        "message": str(e)
                    },
                    "data": {}
                }
            # 未发生异常, 生成token, 加入白名单，token分发
            else:
                token = utils.generate_token(str(user.id))
                # redis白名单维护
                # redis_conn = utils.get_redis_Connection()
                # redis_conn.set(user.id, token)
                # redis_conn.expire(user.id, 43200)
                return {
                    "code": "200",
                    "error": {},
                    "data": {
                        "token": str(token)
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


@blue_print.route('/api/user/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        json_data = json.loads(request.get_data())
        username = json_data.get("username")
        password = json_data.get("password")
        user = db.session.query(User).filter_by(username=username, password=password).first()
        if user is None:
            return {
                "code": "400",
                "error": {
                    "type": "user not found",
                    "message": "username or password is not right"
                },
                "data": {}
            }
        else:
            # 生成token, 加入白名单，token分发
            token = utils.generate_token(str(user.id))
            # redis白名单维护
            # redis_conn = utils.get_redis_Connection()
            # redis_conn.set(user.id, token)
            # redis_conn.expire(user.id, 43200)
            # session['username'] = username
            group_id = "1" if username == 'admin' else "0"
            return {
                "code": "200",
                "error": {},
                "data": {
                    "id": user.id,
                    "group_id": group_id,
                    "token": token
                }
            }
    # if 'username' in session:
    #     return {
    #         "code": "200",
    #         "error": {},
    #         "data": {
    #             "token": "token"
    #         }
    #     }
    # return render_template("login.html")


@blue_print.route('/api/user/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('user_login'))


@blue_print.route('/api/user/modify', methods=['POST', 'GET'])
def user_modify():
    if request.method == 'POST':
        token = request.headers.get("Authorization")
        is_token_valid = utils.certify_token(token) & utils.certify_user_in_Redis(token)
        if is_token_valid is False:
            return {
                "code": "401",
                "error": {
                    "type": "unauthorized",
                    "message": "user not logged in"
                },
                "data": {}
            }
        json_data = json.loads(request.get_data())
        id = json_data.get("id")
        username = json_data.get("username")
        password = json_data.get("password")
        user = db.session.query(User).filter_by(id=id).first()
        if user is None:
            return {
                "code": "401",
                "error": {
                    "type": "user not found",
                    "message": "username or password is not right"
                },
                "data": {}
            }
        else:
            user.username = username
            user.password = password
            user.update_user()
            # user_id = utils.get_user_id_from_token(token)
            # redis_conn = utils.redis_connection
            # redis_conn.delete(user_id)
            return {
                "code": "200",
                "error": {
                    "type": "requires re-login",
                    "message": "Information changed, need to re-login",
                }
            }
    # if 'username' in session:
    #     return {
    #         "code": "200",
    #         "error": {},
    #         "data": {
    #             "token": "token"
    #         }
    #     }
    # return render_template("login.html")


# @blue_print.route('/api/user/logout')
# def logout():
#     # session.pop('username', None)
#     token = request.headers.get("Authorization")
#     is_token_valid = utils.certify_token(token) & utils.certify_user_in_Redis(token)
#     if is_token_valid:
#         user_id = utils.get_user_id_from_token(token)
#         redis_conn = utils.redis_connection
#         redis_conn.delete(user_id)
#     return redirect(url_for('user_login'))