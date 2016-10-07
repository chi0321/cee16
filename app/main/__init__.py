from flask import Blueprint
from ..modles import Permission

main = Blueprint('main',__name__,static_folder='', template_folder='templates', static_url_path='')

from . import views,error
@main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)
