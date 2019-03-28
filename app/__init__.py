from flask import Flask
from flask_restful import Api

from config import Config
from app.user.resources import User, UserRegister, SetPassword, UserLogin
from app.oauth2.resources import GithubLogin, GithubAuthorize
from app.oauth2.base import OauthResource
from app.extensions import db
from app.extensions import ma
from app.extensions import oauth
from app.extensions import jwt


def create_app():
    app = Flask(__name__)
    api = Api(app)
    jwt.init_app(app)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)

    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(UserLogin, '/login')
    # api.add_resource(GithubLogin, '/login/github')
    api.add_resource(SetPassword, '/user/password')
    api.add_resource(OauthResource, '/login/<provider_name>')
    api.add_resource(GithubAuthorize, '/login/github/authorized', endpoint='github.authorize')

    oauth.init_app(app)

    return app
