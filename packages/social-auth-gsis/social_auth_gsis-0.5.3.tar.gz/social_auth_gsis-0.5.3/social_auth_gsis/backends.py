from django.conf import settings
from social_core.backends.oauth import BaseOAuth2
import requests
import xmltodict


class GSISOAuth2(BaseOAuth2):
    """GSIS OAuth 2.0 authentication backend"""

    name = "gsis"
    AUTHORIZATION_URL = "https://www1.gsis.gr/oauth2server/oauth/authorize"
    ACCESS_TOKEN_URL = "https://www1.gsis.gr/oauth2server/oauth/token"
    USER_DATA_URL_URL = "https://www1.gsis.gr/oauth2server/userinfo?format=xml"
    ACCESS_TOKEN_METHOD = "POST"
    DEFAULT_SCOPE = ["read"]
    SCOPE_SEPARATOR = ","
    allow_new_users = True

    def get_redirect_uri(self, state=None):
        return settings.SOCIAL_AUTH_GSIS_REDIRECT_URL

    def get_username_by_tax_id(self, tax_id):
        return f"gsis-{tax_id}"

    def auth_complete_params(self, state=None):
        auth_complete_params = super().auth_complete_params(state=state)
        auth_complete_params["state"] = state
        auth_complete_params["scope"] = "read"
        return auth_complete_params

    def request_access_token(self, *args, **kwargs):
        url = args[0]
        response = requests.request(url=url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_user_details(self, response):
        user_details = {
            "username": response["username"],
            "first_name": response["first_name"],
            "last_name": response["last_name"],
            "tax_id": response["tax_id"],
        }
        return user_details

    def user_data(self, access_token, *args, **kwargs):
        user_data_headers = {"Authorization": f"Bearer {access_token}"}
        user_data_response = requests.get(
            self.USER_DATA_URL,
            headers=user_data_headers,
        )
        user_data_response.raise_for_status()
        user_data = xmltodict.parse(user_data_response.text)
        tax_id = user_data["root"]["userinfo"]["@taxid"].strip()
        username = self.get_username_by_tax_id(tax_id)
        first_name = user_data["root"]["userinfo"]["@firstname"].strip()
        last_name = user_data["root"]["userinfo"]["@lastname"].strip()
        response = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "tax_id": tax_id,
        }
        return response

    def get_user_id(self, details, response):
        tax_id = response.get("tax_id")
        return self.get_username_by_tax_id(tax_id)


class GSISOAuth2Testing(GSISOAuth2):
    """GSIS OAuth 2.0 testing authentication backend"""

    name = "gsis_testing"
    AUTHORIZATION_URL = "https://test.gsis.gr/oauth2server/oauth/authorize"
    ACCESS_TOKEN_URL = "https://test.gsis.gr/oauth2server/oauth/token"
    USER_DATA_URL_URL = "https://test.gsis.gr/oauth2server/userinfo?format=xml"


class GSISOTPOAuth2(GSISOAuth2):
    """GSIS OAuth 2.0 authentication backend with OTP"""

    name = "gsis_otp"
    AUTHORIZATION_URL = "https://www1.gsis.gr/oauth2serverotp/oauth/authorize"
    ACCESS_TOKEN_URL = "https://www1.gsis.gr/oauth2serverotp/oauth/token"
    USER_DATA_URL_URL = "https://www1.gsis.gr/oauth2serverotp/userinfo?format=xml"

    def get_redirect_uri(self, state=None):
        return settings.SOCIAL_AUTH_GSIS_OTP_REDIRECT_URL


class GSISOTPOAuth2Testing(GSISOTPOAuth2):
    """GSIS OAuth 2.0 testing authentication backend with OTP"""

    name = "gsis_otp_testing"
    AUTHORIZATION_URL = "https://test.gsis.gr/oauth2serverotp/oauth/authorize"
    ACCESS_TOKEN_URL = "https://test.gsis.gr/oauth2serverotp/oauth/token"
    USER_DATA_URL_URL = "https://test.gsis.gr/oauth2serverotp/userinfo?format=xml"


class GSISPAOAuth2(GSISOAuth2):
    """GSIS OAuth 2.0 authentication backend for Public Administration"""

    name = "gsis_pa"
    AUTHORIZATION_URL = "https://www1.gsis.gr/oauth2servergov/oauth/authorize"
    ACCESS_TOKEN_URL = "https://www1.gsis.gr/oauth2servergov/oauth/token"
    USER_DATA_URL_URL = "https://www1.gsis.gr/oauth2servergov/userinfo?format=xml"
    allow_new_users = False

    def get_redirect_uri(self, state=None):
        return settings.SOCIAL_AUTH_GSIS_PA_REDIRECT_URL

    def get_username_by_tax_id(self, tax_id):
        return f"gsis-pa-{tax_id}"


class GSISPAOAuth2Testing(GSISPAOAuth2):
    """GSIS OAuth 2.0 testing authentication backend for Public Administration"""

    name = "gsis_pa_testing"
    AUTHORIZATION_URL = "https://test.gsis.gr/oauth2servergov/oauth/authorize"
    ACCESS_TOKEN_URL = "https://test.gsis.gr/oauth2servergov/oauth/token"
    USER_DATA_URL_URL = "https://test.gsis.gr/oauth2servergov/userinfo?format=xml"
