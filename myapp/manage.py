from flask import (
    Blueprint,flash,g,redirect,render_template,request,url_for
)
from myapp.auth import login_required
from myapp.db import get_db
from werkzeug.exceptions import abort

bp = Blueprint('manage',__name__,url_prefix="/manage")


@bp.route('/hello')
def hello():
    return "hello"