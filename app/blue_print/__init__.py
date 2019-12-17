from flask import Blueprint
# 实例化 Blueprint 类，两个参数分别为蓝本的名字和蓝本所在包或模块，第二个通常填 __name__ 即可
blue_print = Blueprint('blue_print', __name__)

# 放在底部防止循环引用
from . import route, route_article, errors, route_comment
