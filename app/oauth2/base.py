from flask import current_app, url_for, request, redirect
from flask_restful import Resource
from app.extensions import oauth, github


class OauthSignIn:
    """
    Base class defines the structure that the subclasses that implement provider must follow.
    """
    providers = None

    def __init__(self, provider_name):
        """
        Initializes the provider's name, app id and app secret, which
        are obtained from the configuration

        Ex:
        app.config['OAUTH_CREDENTIALS'] = {
            'github': {
                'id':     the app id,
                'secret': the app secret
            }
        }

        :param provider_name: provider's name
        """
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        # Subclasses must implement this method
        # Redirect to the provider's website to let user authenticate there
        pass

    def callback(self):
        # Subclasses must implement this method
        # Once the authentication is completed the provider redirects back to the application.
        pass

    def get_call_back_url(self):
        # It will be redirecting to a URL that will call it
        # The URL that the provider needs to redirect to is returned by the get_callback_url() method
        # and is built using the provider name, so that each provider gets its own dedicated route.
        return url_for('oauth_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = dict()
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class GithubSignIn(OauthSignIn):
    def __init__(self):
        super(GithubSignIn, self).__init__(provider_name='github')
        self.service = github

    def authorize(self):
        return self.service.authorize(url_for('github.authorize', _external=True))


class OauthResource(Resource):
    @classmethod
    def get(cls, provider_name):
        oauth = OauthSignIn.get_provider(provider_name)
        return oauth.authorize()

