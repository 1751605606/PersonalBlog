# 导入蓝本 blue_print
from . import blue_print
from flask import *
import json
from app.models import *
from app import db


@blue_print.route('/api/article', methods=['POST'])
def post_article():
    if request.method == 'POST':
        # 验证token

        # 存储文章
        json_data = json.loads(request.get_data())
        title = json_data.get("title")
        text = json_data.get("text")
        article = Article(None, title, text)
        try:
            article.add_article()
            return {
                "code": "200",
                "error": {},
                "data": {
                    "id": article.id
                }
            }
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
                    "text": article.text
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


@blue_print.route('/api/articles', methods=['GET'])
def get_articles():
    if request.method == 'GET':
        # 查询数据库返回文章
        result = db.session.query(Article).all()
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