from json import dumps
from uuid import uuid4

from clients.base_client import BaseClient

from config import BASE_URI_PEOPLE_API
from utils.request import APIRequest


class PeopleClient(BaseClient):
    def __init__(self):
        super().__init__()

        self.base_url = BASE_URI_PEOPLE_API
        self.request = APIRequest()

    def create_person(self, body=None):
        last_name, response = self.__create_person_with_unique_last_name(body)
        return last_name, response

    def read_all_persons(self):
        response = self.request.get(self.base_url)
        return response

    def one_person_by_id(self, person_id):
        pass

    def update_person(self, person_id):
        pass

    def delete_person(self, person_id):
        pass

    def __create_person_with_unique_last_name(self, data=None):
        if data is None:
            last_name = f'User {uuid4()}'
            payload = dumps({
                'fname': 'New',
                'lname': last_name
            })
        else:
            last_name = data['lname']
            payload = dumps(data)

        response = self.request.post(self.base_url, data, self.headers)
        return last_name, response
