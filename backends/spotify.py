from social_core.backends.oauth import BaseOAuth2
from collect_service.settings import SOCIAL_AUTH_SPOTIFY_KEY, SOCIAL_AUTH_SPOTIFY_SECRET
import base64
from social_core.utils import handle_http_errors

class SpotifyCustomOAuth2(BaseOAuth2):
    name = 'spotify'
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'
    ACCESS_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ' '
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token'),
    ]

    def auth_headers(self):
        auth_str = '{0}:{1}'.format(*self.get_key_and_secret())
        b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
        return {
            'Authorization': 'Basic {0}'.format(b64_auth_str)
        }

    def get_user_details(self, response):
        """Return user details from Spotify account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('display_name')
        )
        return {'username': response.get('id'),
                'email': response.get('email'),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://api.spotify.com/v1/me',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )

    # name = "custom_spotify"
    # ID_KEY = 'id'
    # AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'
    # ACCESS_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    # ACCESS_TOKEN_METHOD = 'POST'

    # @handle_http_errors
    # def auth_complete(self, *args, **kwargs):
    #     """Completes login process, must return user instance"""
    #     self.process_error(self.data)
    #     state = self.validate_state()
    #     data, params = None, None
    #     if self.ACCESS_TOKEN_METHOD == 'GET':
    #         params = self.auth_complete_params(state)
    #     else:
    #         data = self.auth_complete_params(state)

    #     response = self.request_access_token(
    #         self.access_token_url(),
    #         data=data,
    #         params=params,
    #         headers=self.auth_headers(),
    #         auth=self.auth_complete_credentials(),
    #         method=self.ACCESS_TOKEN_METHOD
    #     )
    #     self.process_error(response)
    #     return self.do_auth(response['access_token'], response=response,
    #                         *args, **kwargs)

    # @handle_http_errors
    # def do_auth(self, access_token, *args, **kwargs):
    #     """Finish the auth process once the access_token was retrieved"""
    #     data = self.user_data(access_token, *args, **kwargs)
    #     response = kwargs.get('response') or {}
    #     response.update(data or {})
    #     if 'access_token' not in response:
    #         response['access_token'] = access_token
    #     kwargs.update({'response': response, 'backend': self})
    #     return self.strategy.authenticate(*args, **kwargs)

    # def refresh_token_params(self, token, *args, **kwargs):
    #     client_id, client_secret = self.get_key_and_secret()
    #     return {
    #         'refresh_token': token,
    #         'grant_type': 'refresh_token',
    #         'client_id': client_id,
    #         'client_secret': client_secret
    #     }

    # def auth_headers(self):
    #     auth_str = '{0}:{1}'.format(*self.get_key_and_secret())
    #     b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
    #     return {
    #         'Authorization': 'Basic {0}'.format(b64_auth_str)
    #     }

    # def get_key_and_secret(self):
    #     print(self.setting('SOCIAL_AUTH_SPOTIFY_KEY'), self.setting('SOCIAL_AUTH_SPOTIFY_SECRET'))
    #     return self.setting('SOCIAL_AUTH_SPOTIFY_KEY'), self.setting('SOCIAL_AUTH_SPOTIFY_SECRET')


    # def get_user_names(self, fullname='', first_name='', last_name=''):
    #     fullname = fullname or ''
    #     first_name = first_name or ''
    #     last_name = last_name or ''
    #     if fullname and not (first_name or last_name):
    #         try:
    #             first_name, last_name = fullname.split(' ', 1)
    #         except ValueError:
    #             first_name = first_name or fullname or ''
    #             last_name = last_name or ''
    #     fullname = fullname or ' '.join((first_name, last_name))
    #     return fullname.strip(), first_name.strip(), last_name.strip()


    # def user_data(self, access_token, *args, **kwargs):
    #     """Loads user data from service"""
    #     return self.get_json(
    #         'https://api.spotify.com/v1/me',
    #         headers={'Authorization': 'Bearer {0}'.format(access_token)}
    #     )

    
    # def get_user_details(self, response):
    #     """Return user details from Spotify account"""
    #     fullname, first_name, last_name = self.get_user_names(
    #         response.get('display_name')
    #     )
    #     return {'username': response.get('id'),
    #             'email': response.get('email'),
    #             'fullname': fullname,
    #             'first_name': first_name,
    #             'last_name': last_name}