import json
from relari.core.types import HTTPMethod
from relari.core.exceptions import APIError

class ProjectsClient:
    def __init__(self, client):
        self._client = client

    def list(self):
        response = self._client._request("projects", HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to list projects", response=response)
        return response.json()

    def create(self, name: str):
        payload = {"name": name}
        response = self._client._request(
            "projects", HTTPMethod.POST, data=json.dumps(payload)
        )
        if response.status_code != 200:
            raise APIError(message="Failed to create project", response=response)
        return response.json()

    def find(self, name: str):
        projects = self.list()
        name = name.strip()
        for project in projects:
            if project["name"].strip() == name:
                return project
        return None