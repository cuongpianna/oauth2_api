import os


class Config:
    SECRET_KEY = 'porn'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "example.db"))

    OAUTH_CREDENTIALS = {
        'github': {
            'id': '1d2e6c5ccc6fa961ee81',
            'secret': '26c6bf8c5b4ccede0170889b9ca68f517a0004d7'
        },
        'facebook': {
            'id': '2122380331378948',
            'secret': 'c9fc851fcfcaf76118ed28d1fb804a4d'
        }
    }
