from assertpy import assert_that

from utils.request import Response


def assert_people_response_has_person_with_first_name(response: Response, first_name):
    assert_that(response.as_dict).extracting('fname').is_not_empty().contains(first_name)
