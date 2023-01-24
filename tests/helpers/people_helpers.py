from jsonpath_ng import parse


def search_created_user_by_last_name(people, last_name):
    return [person for person in people if person['lname'] == last_name].pop()


def search_nodes_using_json_path(people, json_path):
    json_path_expr = parse(json_path)
    return [match.value for match in json_path_expr.find(people)]
