# 导入蓝本 blue_print
from . import blue_print
from flask import *
import json
from app.models import *
from app import db

'''
有id：文章存在则修改，不存在则添加
无：添加
'''
@blue_print.route('/api/article', methods=['POST'])
def post_article():
    if request.method == 'POST':
        # 验证token

        # 存储文章
        json_data = json.loads(request.get_data())
        id = json_data.get('id')
        title = json_data.get("title")
        text = json_data.get("text")
        article = Article(None, title, text, 0, 0, 0)
        try:
            if id is None:
                article.add_article()
                return {
                    "code": "200",
                    "error": {},
                    "data": {
                        "id": article.id
                    }
                }
            else:
                result = db.session.query(Article).filter_by(id=id).first()
                if result is None:
                    article.add_article()
                    return {
                        "code": "200",
                        "error": {},
                        "data": {
                            "id": article.id
                        }
                    }
                else:
                    result = article
                    result.update_article()
        except Exception as e:
            return {
                "code": "200",
                "error": {
                    'type': "exception occur",
                    'message': str(e)
                },
                "data": {}
            }


@blue_print.route('/api/article/<article_id>', methods=['GET'])
def get_article_by_id(article_id):
    if request.method == 'GET':
        # 查询数据库返回文章
        article = db.session.query(Article).filter_by(id=article_id).first()
        if article is None:
            return {
                "code": "200",
                "error": {
                    "type": "article not found",
                    "message": "article " + article_id + " does not exist"
                },
                "data": {}
            }
        else:
            return {
                "code": "200",
                "error": {},
                "data": {
                    "id": article.id,
                    "title": article.title,
                    "text": article.text,
                    "view_number": article.view_number,
                    "like_number": article.like_number,
                    "comment_number": article.comment_number
                }
            }


@blue_print.route('/api/article/<article_id>', methods=['DELETE'])
def delete_article_by_id(article_id):
    if request.method == 'DELETE':
        # 验证token
        # 数据库删除文章
        article = db.session.query(Article).filter_by(id=article_id).first()
        if article is None:
            return {
                "code": "200",
                "error": {
                    "type": "article not found",
                    "message": "article " + article_id + " does not exist"
                },
                "data": {}
            }
        else:
            try:
                article.delete_article()
                return {
                    "code": "200",
                    "error": {},
                    "data": {}
                }
            except Exception as e:
                return {
                    "code": "200",
                    "error": {
                        "type": "exception occur",
                        "message": str(e)
                    },
                    "data": {}
                }


@blue_print.route('/api/article', methods=['GET'])
def get_articles():
    if request.method == 'GET':
        # 查询数据库返回文章
        index = 0 if request.args.get('index') is None else request.args.get('index')
        size = 0 if request.args.get('size') is None else request.args.get('size')
        result = db.session.query(Article).offset(index).limit(size).all()
        articles_list = []
        for article in result:
            article = {
                'id': article.id,
                'title': article.title,
                'text':  article.text
            }
            articles_list.append(article)
        response = {
            'code': '200',
            'error': {},
            'data': articles_list
        }
        return json.dumps(response)


@blue_print.route('/api/article/<article_id>/view', methods=['POST'])
def view_article(article_id):
    if request.method == 'POST':
        article = db.session.query(Article).filter_by(id=article_id).first()
        if Article is None:
            return {
                "code": "200",
                "error": {
                    "type": "article not found",
                    "message": "article " + article_id + " does not exist"
                },
                "data": {}
            }
        else:
            article.view_article()
            return {
                "code": "200",
                "error": {},
                "data": {
                    "view_number": article.view_number
                }
            }


@blue_print.route('/api/article/<article_id>/like', methods=['POST'])
def like_article(article_id):
    if request.method == 'POST':
        article = db.session.query(Article).filter_by(id=article_id).first()
        if Article is None:
            return {
                "code": "200",
                "error": {
                    "type": "article not found",
                    "message": "article " + article_id + " does not exist"
                },
                "data": {}
            }
        else:
            article.like_article()
            return {
                "code": "200",
                "error": {},
                "data": {
                    "like_number": article.like_number
                }
            }