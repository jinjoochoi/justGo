from flask import Blueprint

kakao_messenger = Blueprint('kakao_messenger', __name__)

from . import views
