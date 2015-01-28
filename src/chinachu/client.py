# encoding=utf-8
import requests
from requests.auth import HTTPBasicAuth
import json


class AuthenticationException(Exception):
    pass
class ChinachuException(Exception):
    pass

class Client(object):

    def __init__(self, base_uri, username, password):
        self.base_url = base_uri
        self.auth = HTTPBasicAuth(username, password)

    def get_resources(self, name, id=None, query={}):

        if id:
            url = "{0}/{1}/{2}.json".format(self.base_url, name, id)
        else:
            url = "{0}/{1}.json".format(self.base_url, name)

        response = requests.get(url, auth=self.auth)

        if response.status_code == 401:
            raise AuthenticationException()
        elif response.status_code != 200:
            raise ChinachuException()

        data = json.loads(response.text)
        return data

    def get_recorded(self, id=None, query={}):
        return self.get_resources("recorded", id, query)

