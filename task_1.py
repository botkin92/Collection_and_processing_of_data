import requests
import json
from pprint import pprint


def list_repos(user):
    response = requests.get(f'https://api.github.com/users/{user}/repos')
    json_data = response.json()
    return json_data


def file_writer(json_data):
    with open('list_repo_json', 'w') as file:
        json.dump(json_data, file, indent=2)


def only_names_repos(json_data):
    names_repos = []
    for el in json_data:
        names_repos.append(el["name"])
    # list_names_repos = {"name": names_repos}
    return names_repos


repos_request = list_repos('Yorko')
file_writer(repos_request)
pprint(only_names_repos(repos_request))
