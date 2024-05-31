"""
This module is a wrapper for calling Open API Service inside connectwise VPC.
which authenticates using clientId and clientSecret and provides methods to call
ASIO integrated resources and external resources to RPA MS
It provides methods to call ASIO integrated resources and external resources to RPA MS

Questions:
How can partner use this service, without integration map, client id and client secret in his
local environment file.

1) fetch input data
2) validate attributes


integration_map = {
    'microsoft_graph' : "https://graph.microsoft.com/",
    'o365' : "https://outlook.office.com/",
}


"""


import os
import json
import datetime
import requests
from urllib.parse import urlparse, urljoin


class CWHTTPRequestHelper:

    """_summary_
    integration_map: dict
        A dictionary containing the integration map

    need to serve 3 types of requests.
        1) ConnectWise Open API services
        2) RPA-MS Proxy requests ==> integration_map
        3) external requests

    """

    _routes = {
        "open_api_rpa_ms_proxy": "/api/platform/v1/rpa/resolve"
    }

    _integration_map_default = {
        "microsoft_csp": "https://graph.microsoft.com"
    }

    def __init__(self, **kwargs):
        data_from_input_file: dict = self.__fetch_input_data()
        self.__cw_open_api_client_id: str = data_from_input_file.get(
            "cwOpenAPIClientId", None)
        self.__cw_open_api_client_secret: str = data_from_input_file.get(
            "cwOpenAPIClientSecret", None)
        self.__cw_company_id: str = data_from_input_file.get(
            "cwCompanyId", None)
        self.__cw_site_id: str = data_from_input_file.get("cwSiteId", None)
        self.__integration_map: dict = data_from_input_file.get(
            'integrationMap', self._integration_map_default)
        self.__integration_map_reversed = {
            v: k for k, v in self.__integration_map.items()}
        self.__cw_patner_api_scope = data_from_input_file.get(
            "cwPartnerAPIScope", None)
        self.__connection_id = kwargs.get("connection_id", "")
        self.__cw_open_api_url = data_from_input_file.get("cwOpenAPIURL", "")
        self.__open_api_access_token = None
        self.__open_api_token_response = None
        self.__open_api_token_expires_in = None
        self.__verify_attributes()

    def __verify_attributes(self):
        # uncomment the below when there is a support for integration map
        # if not self.__integration_map:
        #     raise ValueError('"integrationMap" not found.')
        if not self.__cw_open_api_client_id:
            raise ValueError('"cwOpenAPIClientId" not found.')
        if not self.__cw_open_api_client_secret:
            raise ValueError('"cwOpenAPIClientSecret" not found.')
        if not self.__cw_company_id:
            raise ValueError('"cwCompanyId" not found.')
        if not self.__cw_site_id:
            raise ValueError('"cwSiteId" not found.')
        if not self.__cw_patner_api_scope:
            raise ValueError(
                '"cwPartnerAPIScope" not found in the "input.json" file.')
        if not self.__cw_open_api_url:
            raise ValueError(
                '"cwOpenAPIURL" not found. in the "input.json" file.')

    def __fetch_input_data(self, input_file: str = 'input.json'):

        if not os.path.exists(input_file):
            raise FileNotFoundError('"input.json" file not found.')

        with open(input_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as jsde:
                raise jsde('input.json is not in correct format.')
            return data

    def acquire_access_token(self) -> str:
        url = urljoin(self.__cw_open_api_url, "/v1/token")
        scopes = " ".join(self.__cw_patner_api_scope)
        data = {
            "grant_type": "client_credentials",
            "client_id": self.__cw_open_api_client_id,
            "client_secret": self.__cw_open_api_client_secret,
            "scope": scopes
        }
        headers = {"Content-Type": "application/json"}
        # todo: remove verify=False for Open API requests in production environment
        response = requests.post(
            url, json=data, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f'Unable to get access token.\n{response.status_code}. {response.text}')

        # assigned token response to calculate token expiration and other response information if needed.
        self.__open_api_token_response = response.json()
        self.__open_api_access_token = self.__open_api_token_response.get(
            'access_token', None)
        self.__open_api_token_expires_in = datetime.datetime.now() + \
            datetime.timedelta(
                seconds=self.__open_api_token_response.get('expires_in', 0) - 10)
        return self.__open_api_access_token

    @property
    def _is_token_expired(self) -> bool:
        return datetime.datetime.now() > self.__open_api_token_expires_in if self.__open_api_token_expires_in else True

    def _add_authorization_header_to_kwargs(self, kwargs) -> dict:
        if self.__open_api_access_token is None or self._is_token_expired:
            _ = self.acquire_access_token()

        headers = kwargs.get('headers', {})
        if not headers.get('Authorization', None):
            headers['Authorization'] = f'Bearer {self.__open_api_access_token}'
        updated_kwargs = kwargs.copy()
        updated_kwargs['headers'] = headers
        # updated_kwargs['verify'] = False
        return updated_kwargs

    def _rpa_ms_proxy_request(self, method, url, **kwargs) -> requests.Response:
        """ prepares a proxy request to rpa-microservice

            request body reference

            req_body = {
                "integrationName": "string",
                "connectionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6", # it can be empty
                "resource_list": [
                    "string"
                ], # resource list is the base url of the api endpoint ex. first part "https://graph.microsoft.com" second part "/v1.0/me"
                "method": "string",
                "url": "string",
                "body": "string",
                "clientId": "string",  # cwCompanyId to be passed here
                "siteId": "string"  # cwSiteId to be passed here
            }
        """
        _proxy_url: str = urljoin(
            self.__cw_open_api_url, self._routes.get('open_api_rpa_ms_proxy'))
        parsed_url: str = urlparse(url)
        base_url: str = f"{parsed_url.scheme}://{parsed_url.netloc}".lower()
        # url_path: str = url.split(base_url)[-1]
        integration_name: str = self.__integration_map_reversed.get(
            base_url, None)

        if not integration_name:
            raise ValueError('Integration name not found.')

        resource_list: list = []
        resource_list.append(base_url)

        req_body: dict = {
            "integrationName": integration_name,
            "connectionId": self.__connection_id,
            "method": method.upper(),
            "resourceList": resource_list,
            "url": url,
            "clientId": self.__cw_company_id,  # cwCompanyId to be passed here
            "siteId": self.__cw_site_id  # cwSiteId to be passed here
        }

        data = kwargs.get('data', None)
        if data:
            req_body['body'] = json.loads(data)

        body_as_json_dict = kwargs.get('json', None)
        if body_as_json_dict:
            req_body['body'] = body_as_json_dict

        kwargs["data"] = json.dumps(req_body)
        kwargs = self._add_authorization_header_to_kwargs(kwargs)
        return requests.request('POST', url=_proxy_url, **kwargs)

    def _open_api_request(self, method, url, **kwargs) -> requests.Response:
        kwargs = self._add_authorization_header_to_kwargs(kwargs)
        response = requests.request(method, url, **kwargs)
        return response

    def request(self, method, url, **kwargs) -> requests.Response:
        print(kwargs)
        parsed_url: str = urlparse(url)
        base_url: str = f"{parsed_url.scheme}://{parsed_url.netloc}".lower()
        open_api_base_url: str = self.__cw_open_api_url.lower()

        if base_url == open_api_base_url:
            # open api requests
            response = self._open_api_request(method, url, **kwargs)
        elif base_url in self.__integration_map_reversed:
            # integrated requests
            response = self._rpa_ms_proxy_request(method, url, **kwargs)
        else:
            # generic requests
            response = requests.request(method, url, **kwargs)

        return response


class CWHTTPRequest:
    """This class is a wrapper for calling Open API Service outside connectwise VPC."""

    def __init__(self, **kwargs):
        self.__request_helper = CWHTTPRequestHelper(**kwargs)
        self.__access_token = None

    @property
    def access_token(self):
        """returns connectwise open api service access token
        Returns:
            str: returns access token
        """
        if not self.__access_token:
            self.__access_token = self.__request_helper.acquire_access_token()
        return self.__access_token

    def request(self, method, url, **kwargs):
        return self.__request_helper.request(method, url=url, **kwargs)

    def get(self, url, params=None, **kwargs):
        return self.__request_helper.request(method='GET', url=url, params=params, **kwargs)

    def post(self, url, data = None, json: dict = None, **kwargs):
        return self.__request_helper.request(method='POST', url=url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.__request_helper.request(method='PUT', url=url, data=data,  **kwargs)

    def patch(self, url,  data=None, **kwargs):
        return self.__request_helper.request(method='PATCH', url=url, data=data,  **kwargs)

    def delete(self, url, **kwargs):
        return self.__request_helper.request(method='DELETE', url=url, **kwargs)

    def head(self, url, **kwargs):
        return self.__request_helper.request(method='HEAD', url=url, **kwargs)

    def options(self, url, **kwargs):
        return self.__request_helper.request(method='OPTIONS', url=url, **kwargs)
