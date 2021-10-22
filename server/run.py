import datetime
from flask import Flask, render_template, url_for, request, send_from_directory
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from flask_restful import Api
from flask_sitemap import Sitemap
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import os
import config
from flask_cors import CORS

from server.data.test_api import TestResourceUsual, TestResourcePost

ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
application = Flask(__name__)
cors = CORS(application, resources={r"/api/*": {"origins": "*"}})

api = Api(application)
api.add_resource(TestResourceUsual, "/api/test")
api.add_resource(TestResourcePost, "/api/test/<string:some_data>")

ext = Sitemap(app=application)
application.config.from_object(config)

# db_session.global_init("db/.sqlite")
# login_manager = LoginManager()
# login_manager.init_app(application)


def get_render_template(template_name, title, **kwargs):
    return render_template(template_name, title=title, **kwargs)


def main(port=8000):
    application.run(port=port, debug=True)


@application.route("/members")  # members
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


# Стартовая страница
@application.route("/")
def website_main_page():
    return get_render_template("main-page.html", title="главная страница")


if __name__ == '__main__':
    main(port=8000)
