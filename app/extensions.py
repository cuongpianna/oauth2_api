from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_oauthlib.client import OAuth
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

oauth = OAuth()
github = oauth.remote_app(
    'github',
    consumer_key='1d2e6c5ccc6fa961ee81',
    consumer_secret='26c6bf8c5b4ccede0170889b9ca68f517a0004d7',
    request_token_params={"scope": "user:email"},
    base_url="https://api.github.com/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize"
)


@github.tokengetter
def get_github_token():
    if 'access_token' in g:
        return g.access_token
