# 导入蓝本 blue_print
from . import blue_print
from flask import *
import json
from app.models import *
from app import db
from sqlalchemy import func
import jieba

'''
发布/修改文章
有id：文章存在则修改，不存在则添加
无：添加
'''
@blue_print.route('/api/article', methods=['POST'])
def post_article():
    if request.method == 'POST':
        # 验证token
        # if not token_true() :
        #   return {
        #       "code": "200",
        #       "error": {
        #           'type': "operation is rejected",
        #           'message': "you have no right to operate"
        #       },
        #       "data": {}
        #   }
        # 存储文章
        json_data = json.loads(request.get_data())
        id = json_data.get('id')
        title = json_data.get("title")
        text = json_data.get("text")
        classname = json_data.get("classname")
        # 用'\t'连接labels数组的前五个标签
        if json_data.get("labels") is not None:
            labels = "\t".join(json_data.get("labels")[:5])
        else:
            labels = ""
        try:
            # 没有上传classname, 添加到默认分类classname = None
            classname_id = None
            if classname is not None:
                if classname.strip() != "":
                    result = db.session.query(ClassName).filter_by(name=classname.strip()).first()
                    # classname 不存在,创建classname
                    if result is None:
                        temp = ClassName(classname.strip())
                        temp.add_classname()
                        classname_id = temp.id
                    else:
                        classname_id = result.id
                else:
                    return {
                        "code": "200",
                        "error": {
                            "type": "argument error",
                            "message": "classname can not be null"
                        }
                    }
                    pass
            if id is None:
                # 创建新的文章
                article = Article(None, title, text, classname_id, labels, 0, 0, 0)
                article.add_article()
                return {
                    "code": "200",
                    "error": {},
                    "data": {
                        "id": article.id
                    }
                }
            else:
                # 修改文章信息
                result = db.session.query(Article).filter_by(id=id).first()
                result.title = title
                result.text = text
                result.classname_id = classname_id
                result.labels = labels
                result.update_article()
                return {
                    "code": "200",
                    "error": {},
                    "data": {
                        "id": result.id
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

# 获取特定文章
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
            classname = db.session.query(ClassName).filter_by(id=article.classname_id).first()
            return {
                "code": "200",
                "error": {},
                "data": {
                    "id": article.id,
                    "title": article.title,
                    "text": article.text,
                    "view_number": article.view_number,
                    "like_number": article.like_number,
                    "comment_number": article.comment_number,
                    "classname": classname.name if classname is not None else None,
                    "labels": article.labels.split("\t")[:5] if article.labels.strip() != "" else []
                }
            }

# 删除特定文章
@blue_print.route('/api/article/<article_id>', methods=['DELETE'])
def delete_article_by_id(article_id):
    if request.method == 'DELETE':
        # 验证token
        # if not token_true() :
        #   return {
        #       "code": "200",
        #       "error": {
        #           'type': "operation is rejected",
        #           'message': "you have no right to operate"
        #       },
        #       "data": {}
        #   }
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

# 批量获取文章
@blue_print.route('/api/article', methods=['GET'])
def get_articles():
    if request.method == 'GET':
        # 查询数据库返回文章
        index = 0 if request.args.get('index') is None else request.args.get('index')
        size = request.args.get('size')
        classname = request.args.get('classname')
        articles = []
        if classname is None:
            if size is not None:
                articles = db.session.query(Article).offset(index).limit(size).all()
            else:
                articles = db.session.query(Article).offset(index).all()
        else:
            classname_id = None
            result = db.session.query(ClassName).filter_by(name=classname.strip()).first()
            # classname 不存在
            if result is None:
                return {
                    'code': '200',
                    'error': {
                        "type": "classname not found",
                        "message": "classname " + classname + "does not exist"
                    },
                    'data': {}
                }
            else:
                classname_id = result.id
                if size is not None:
                    articles = db.session.query(Article).filter_by(classname_id=classname_id).offset(index).limit(size).all()
                else:
                    articles = db.session.query(Article).filter_by(classname_id=classname_id).offset(index).all()
        articles_list = []
        for temp in articles:
            name = db.session.query(ClassName).filter_by(id=temp.classname_id).first()
            articles_list.append({
                "id": temp.id,
                "title": temp.title,
                "text": temp.text,
                "view_number": temp.view_number,
                "like_number": temp.like_number,
                "comment_number": temp.comment_number,
                "classname": name.name if name is not None else None,
                "labels": temp.labels.split("\t")[:5] if temp.labels.strip() != "" else []
            })
        response = {
            'code': '200',
            'error': {},
            'data': articles_list
        }
        return json.dumps(response)

# 增加文章阅读量
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

# 点赞文章
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


# 搜索文章
@blue_print.route('/api/article/search', methods=['GET'])
def search_article():
    if request.method == 'GET':
        # 查询数据库返回文章
        index = 0 if request.args.get('index') is None else request.args.get('index')
        size = request.args.get('size')
        classname = request.args.get('classname')
        keyword = request.args.get('keyword').split() if request.args.get('keyword') is not None else None
        if classname is None:
            if size is not None:
                query_result = db.session.query(Article).offset(index).limit(size).all()
            else:
                query_result = db.session.query(Article).offset(index).all()
        else:
            classname_id = None
            result = db.session.query(ClassName).filter_by(name=classname.strip()).first()
            # classname 不存在
            if result is None:
                return {
                    'code': '200',
                    'error': {
                        "type": "classname not found",
                        "message": "classname " + classname + " does not exist"
                    },
                    'data': {}
                }
            else:
                classname_id = result.id
            if size is not None:
                query_result = db.session.query(Article).filter_by(classname_id=classname_id).offset(index).limit(size).all()
            else:
                query_result = db.session.query(Article).filter_by(classname_id=classname_id).offset(index).all()
        article_list = []
        for temp in query_result:
            name = db.session.query(ClassName).filter_by(id=temp.classname_id).first()
            if keyword is not None:
                # 标签 正文 类别名
                str = temp.labels + " " + (name.name if name.name is not None else "") + " " + temp.text
                # jieba分词搜索
                article_keyword = jieba.cut_for_search(str)
                # return {
                #     "1": list(set(article_keyword))
                # }
                if set(keyword) <= set(article_keyword):
                    article_list.append({
                        "id": temp.id,
                        "title": temp.title,
                        "text": temp.text,
                        "view_number": temp.view_number,
                        "like_number": temp.like_number,
                        "comment_number": temp.comment_number,
                        "classname": name.name if name is not None else None,
                        "labels": temp.labels.split("\t")[:5] if temp.labels.strip() != "" else []
                    })
            else:
                article_list.append({
                    "id": temp.id,
                    "title": temp.title,
                    "text": temp.text,
                    "view_number": temp.view_number,
                    "like_number": temp.like_number,
                    "comment_number": temp.comment_number,
                    "classname": name.name if name is not None else None,
                    "labels": temp.labels.split("\t")[:5] if temp.labels.strip() != "" else []
                })
        response = {
            'code': '200',
            'error': {},
            'data': article_list
        }
        return json.dumps(response)


# 获取网站统计信息
@blue_print.route('/api/statistics', methods=['GET'])
def get_statistics():
    if request.method == 'GET':
        article_number = db.session.query(Article).with_entities(func.count(Article.id)).scalar()
        view_number = db.session.query(Article).with_entities(func.sum(Article.view_number)).scalar()
        like_number = db.session.query(Article).with_entities(func.sum(Article.like_number)).scalar()
        comment_number = db.session.query(Article).with_entities(func.sum(Article.comment_number)).scalar()
        user_number = db.session.query(User).with_entities(func.count(User.id)).scalar()
        return {
            'code': '200',
            'error': {},
            'data': {
                'article_number': str(article_number),
                'view_number': str(view_number),
                'like_number': str(like_number),
                'comment_number': str(comment_number),
                'user_number': str(user_number)
            }
        }


# 获取所有文章分类
@blue_print.route('/api/article/classname', methods=['GET'])
def get_all_classname():
    if request.method == 'GET':
        result = db.session.query(ClassName).all()
        name_list = [None]
        for name in result:
            name_list.append(name.name)
        response = {
            'code': '200',
            'error': {},
            'data': list(set(name_list))
        }
        return json.dumps(response)


# 删除文章分类
@blue_print.route('/api/article/classname/<classname>', methods=['DELETE'])
def delete_classname(classname):
    if request.method == 'DELETE':
        # 验证token
        # if not token_true() :
        #   return {
        #       "code": "200",
        #       "error": {
        #           'type': "operation is rejected",
        #           'message': "you have no right to operate"
        #       },
        #       "data": {}
        #   }
        result = db.session.query(ClassName).filter_by(name=classname).first()
        if result is None:
            return {
                "code": "200",
                "error": {
                    "type": "classname not found",
                    "message": "classname " + classname + " does not exist"
                },
                "data": {}
            }
        else:
            articles = db.session.query(Article).filter_by(classname_id=result.id).all()
            try:
                result.delete_classname()
                for article in articles:
                    article.classname_id = None
                    article.update_article()
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