from flask import Blueprint, render_template
from datatracker.models import DailyData
from datatracker.utils import visiblePoints, getDailyData
from flask_login import current_user

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
	return render_template('errorTemplates/404.html'), 404


 
@errors.app_errorhandler(403)
def error_403(error):
	return render_template('errorTemplates/403.html'), 403



@errors.app_errorhandler(500)
def error_500(error):
	return render_template('errorTemplates/500.html'), 500