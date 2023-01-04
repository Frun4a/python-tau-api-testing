import requests
from assertpy import assert_that

from config import BASE_URI
from utils.print_helpers import pretty_print
from uuid import uuid4
from json import dumps


def test_read_all_has_kent():
    response, response_json = get_all_users()
    # pretty_print(response_json)

    print('\nGET - Response status code is {}'.format(response.status_code))
    assert_that(response.status_code).is_equal_to(200)

    first_names = [person['fname'] for person in response_json]
    print('\nNames in the response: {}'.format(', '.join(first_names)))
    assert_that(first_names).contains('Kent')

    # better assertions
    assert_that(response.json()).extracting('fname').is_not_empty().contains('Kent')


def test_new_person_can_be_added():
    last_name, post_response = create_new_user()
    print('\nPOST - Response status code is {}'.format(post_response.status_code))
    assert_that(post_response.status_code).is_equal_to(204)

    get_response = requests.get(BASE_URI)
    get_response_json = get_response.json()
    is_new_user_created = [record['lname'] for record in get_response_json].count(last_name) == 1
    assert_that(is_new_user_created).is_true()


def test_person_can_be_deleted():
    new_user_last_name = create_new_user()[0]
    all_user, _ = get_all_users()
    is_new_user_created = [record['lname'] for record in all_user.json()].count(new_user_last_name) == 1
    assert_that(is_new_user_created).is_true()
    new_user_full_data = [person for person in all_user.json() if person['lname'] == new_user_last_name].pop()
    print('\n')
    print(new_user_full_data)
    person_id_to_be_deleted = new_user_full_data['person_id']

    response = requests.delete(url=f"{BASE_URI}/{person_id_to_be_deleted}")
    assert_that(response.status_code).is_equal_to(200)

    all_user, _ = get_all_users()
    is_new_user_deleted = [record['lname'] for record in all_user.json()].count(new_user_last_name) > 0
    assert_that(is_new_user_deleted).is_false()


def test_person_can_be_updated():
    new_user_last_name = create_new_user()[0]
    all_user, _ = get_all_users()
    is_new_user_created = [record['lname'] for record in all_user.json()].count(new_user_last_name) == 1
    assert_that(is_new_user_created).is_true()
    new_user_full_data = [person for person in all_user.json() if person['lname'] == new_user_last_name].pop()
    print('\n')
    print(new_user_full_data)
    person_id_to_be_updated = new_user_full_data['person_id']

    new_lname = 'Updated' + new_user_full_data['lname']
    payload = dumps({
        'fname': 'Updated New',
        'lname': new_lname
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.put(url=f"{BASE_URI}/{person_id_to_be_updated}", data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(200)

    all_users, _ = get_all_users()
    is_new_user_no_more_has_previous_lname = \
        [record['lname'] for record in all_users.json()].count(new_user_last_name) == 0
    assert_that(is_new_user_no_more_has_previous_lname).is_true()

    is_new_user_has_new_lname = [record['lname'] for record in all_users.json()].count(new_lname) == 1
    assert_that(is_new_user_has_new_lname).is_true()

    new_user_full_data = [person for person in all_users.json() if person['lname'] == new_lname].pop()
    print('\n')
    print(new_user_full_data)

def create_new_user():
    last_name = f'User {uuid4()}'
    payload = dumps({
        'fname': 'New',
        'lname': last_name
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    post_response = requests.post(url=BASE_URI, data=payload, headers=headers)
    return last_name, post_response


def get_all_users():
    response = requests.get(BASE_URI)
    response_json = response.json()
    return response, response_json
