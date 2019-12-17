# 导入蓝本 blue_print
from . import blue_print
from . import errors
from flask import *
import json
import time
from app.models import *
from app import db
from . import utils


"""
评论文章
请求URL：/api/article/{article_id}/comment
请求方式：POST
参数：
参数名	必选	类型	说明
text	是	string	评论文本
"""
@blue_print.route('/api/article/<article_id>/comment', methods=['POST'])
def comment_article(article_id):
    if request.method == 'POST':
        # 验证登录状态
        token = request.headers.get("Authorization")
        is_token_valid = utils.certify_token(token) & utils.certify_user_in_Redis(token)
        if is_token_valid is False:
            return errors.not_logged_in
        # 评论文章
        article = db.session.query(Article).filter_by(id=article_id).first()
        if Article is None:
            return {
                "code": "404",
                "error": {
                    "type": "Not Found",
                    "message": "The article " + article_id + " does not exist"
                },
                "data": {}
            }
        else:
            json_data = json.loads(request.get_data())
            user_id = utils.get_user_id_from_token(token)
            timestamp = int(time.time())
            text = json_data.get("text")
            comment = Comment(None, int(article_id), user_id, text, timestamp)
            comment.add_comment()
            return {
                "code": "200",
                "error": {},
            }


"""
获取文章评论
请求URL：
/api/article/{article_id}/comment
/api/article/{article_id}/?index=INDEX&size=SIZE
请求方式：GET
参数：
参数名	必选	类型	说明
index	否	unsigned int	评论起始index，默认为0
size	否	unsigned int	要返回的评论最大数量，默认为最大
"""
@blue_print.route('/api/article/<article_id>', methods=['GET'])
def get_comment_by_article(article_id):
    if request.method == 'GET':
        # 查询数据库返回文章的评论
        index = 0 if request.args.get('index') is None else request.args.get('index')
        size = request.args.get('size')
        comments = db.session.query(Comment).filter_by(article_id=article_id).all()
        response = {
            'code': '200',
            'error': {},
            'data': {}
        }
        if comments is None:
            # 若没有找到评论，查看是否因为文章不存在
            article = db.session.query(Article).filter_by(id=article_id).first()
            if article is None:
                response = {
                    'code': '404',
                    'error': {
                        "type": "Not Found",
                        "message": "This article not found"
                    },
                    'data':{}
                }
        else:
            comments_list = []
            for comm in comments:
                user = db.session.query(User).filter_by(id=comm.user_id).first()
                timeStamp = comm.timestamp
                timeArray = time.localtime(timeStamp)
                timeString = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                comments_list.append(
                    {
                        'user_id': comm.user_id,
                        'username': user.username,
                        'text': comm.text,
                        'time': timeString
                    }
                )
            response = {
                'code': '200',
                'error': {},
                'data': comments_list
            }
        return json.dumps(response)


"""
获取特定用户的所有评论
请求URL：
/api/user/{user_id}/comment
参数在URI中，是用户id
请求方式：GET
"""
@blue_print.route('/api/user/<user_id>/comment', methods=['GET'])
def get_comment_by_user(user_id):
    if request.method == 'GET':
        # 查询数据库返回用户的所有评论
        comments = db.session.query(Comment).filter_by(user_id=user_id).all()
        response = {
            'code': '200',
            'error': {},
            'data': {}
        }
        if comments is None:
            user = db.session.query(User).filter_by(id=user_id).first()
            # 若没有找到评论，查看是否因为user不存在
            if user is None:
                response = {
                    'code': '404',
                    'error': {
                        "type": "Not Found",
                        "message": "This user not found"
                    },
                    'data': {}
                }
        else:
            comments_list = []
            for comm in comments:
                article = db.session.query(Article).filter_by(id=comm.comment_id).first()
                timeStamp = comm.timestamp
                timeArray = time.localtime(timeStamp)
                timeString = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                if article is not None:
                    comments_list.append(
                        {
                            "article_id": article.id,
                            "article_title": article.title,
                            "text": comm.text,
                            "time": timeString
                        }
                    )
            response = {
                'code': '200',
                'error': {},
                'data': comments_list
            }
        return json.dumps(response)