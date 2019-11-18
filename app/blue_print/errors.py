from flask import render_template
from . import blue_print


@blue_print.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')