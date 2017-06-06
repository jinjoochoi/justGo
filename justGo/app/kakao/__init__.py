from flask import Blueprint
from .manager import APIManager

kakao_messenger = Blueprint('kakao_messenger', __name__)
APIHandler = APIManager()

from . import views
