import requests
import json

from cerberus import Validator
from assertpy import assert_that

from config import BASE_URI_PEOPLE_API

schema = {
    "fname": {'type': 'string'},
    "lname": {'type': 'string'},
    "person_id": {'type': 'number'},
    "timestamp": {'type': 'string'}
}


def test_get_response_schema_for_last_record():
    response = requests.get(BASE_URI_PEOPLE_API)
    response_json = json.loads(response.text)

    validator = Validator(schema, require_all=True)
    is_valid = validator.validate(response_json[-1])

    assert_that(is_valid, validator.errors).is_true()


def test_get_response_schema_for_all_records():
    response = requests.get(BASE_URI_PEOPLE_API)
    response_json = json.loads(response.text)

    validator = Validator(schema, require_all=True)
    for record in response_json:
        is_valid = validator.validate(record)
        assert_that(is_valid, validator.errors).is_true()
