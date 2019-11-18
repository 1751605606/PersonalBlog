# from flask import *
# from flask_sqlalchemy import SQLAlchemy
# import os
# from . import models
# app = Flask(__name__,static_folder=os.path.abspath("./"), static_url_path="")
# app.secret_key = 'team_project'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/personalblog'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# db = SQLAlchemy(app, use_native_unicode='utf8')
# app.run()
#
#
# @app.route('/')
# def index():
#     return render_template("login.html")
#
#
# @app.route('/api/user/login', methods=['POST', 'GET'])
# def user_login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if username == 'admin' and password == 'admin':
#             session['username'] = request.form.get('username')
#             response = make_response({
#                 "code": "200 OK",
#                 "error": {},
#                 "data": {
#                     "token": "n"
#                 }
#             })
#             # 重定向到新的页面
#             return response
#         else:
#             return {
#                 "code": "200 OK",
#                 "error": {
#                     "type": "no such user"
#                 },
#                 "data": {
#                     "token": "n"
#                 }
#             }
#     if 'username' in session:
#         # 重定向到新的页面
#         return {
#                 "code": "200 OK",
#                 "error": {},
#                 "data": {
#                     "token": "n"
#                 }
#             }
#     return render_template("login.html")
#
#
# @app.route('/api/user/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('user_login'))
#
#
# @app.route('/api/articles', methods=['POST'])
# def post_article():
#     if request.method == 'POST':
#         # 验证token
#         title = request.form.get('title')
#         text = request.form.get('text')
#         # 存储文章
#         print(title + text)
#         # 返回
#         response_data = {
#             "code": "200 OK",
#             "error": {},
#             "data": {
#                 "id": "0"
#             }
#         }
#         return response_data
#
#
# @app.route('/api/articles/<article_id>', methods=['GET'])
# def get_article_by_id(article_id):
#     if request.method == 'GET':
#         # 查询数据库返回文章
#         article = {
#             "id":"",
#             "title": "",
#             "text": ""
#         }
#         response_data = make_response({
#             "code": "200 OK",
#             "error": {},
#             "data": article
#         })
#         return response_data
#
#
# @app.route('/api/articles/<article_id>', methods=['DELETE'])
# def delete_article_by_id(article_id):
#     if request.method == 'DELETE':
#         # 验证token
#         # 数据库删除文章
#         response_data = make_response({
#             "code": "200 OK",
#             "error": {}
#         })
#         return response_data
#
#
# @app.route('/api/articles', methods=['GET'])
# def get_articles():
#     if request.method == 'GET':
#         # 查询数据库返回文章
#         articles = [{
#             "id": "",
#             "title": "",
#             "text": ""
#         }]
#         response_data = make_response({
#             "code": "200 OK",
#             "error": {},
#             "data": articles
#         })
#         return response_data
