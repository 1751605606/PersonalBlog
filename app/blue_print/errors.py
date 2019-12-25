from flask import render_template
from . import blue_print


def not_logged_in():
    return {
        "code": "401",
        "error": {
            "type": "User not logged in",
            "message": "Please log in"
        },
        "data": {}
    }


def no_access():
    return {
        "code": "403",
        "error": {
            "type": "User has no right to operate",
            "message": "The current user has no right to edit articles"
        },
        "data": {}
    }


@blue_print.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')