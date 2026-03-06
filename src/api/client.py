"""Base HTTP client for REST API communication."""

import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, path, headers=None):
        return requests.get(self.base_url + path, headers=headers)

    def post(self, path, json, headers=None):
        return requests.post(self.base_url + path, json=json, headers=headers)

    def delete(self, path):
        return requests.delete(self.base_url + path)
