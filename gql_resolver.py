import requests


def resolve(query, headers, *params):
    if len(params) > 0:
            request = requests.post('https://api.github.com/graphql',
                                    json={'query': query, vars: params}, headers=headers)
            if request.status_code == 200:
                return request.json()
            else:
                raise Exception("Query failed to run by returning code of {}. {}".format(
                    request.status_code, query))
    else:
            request = requests.post('https://api.github.com/graphql',
                                json={'query': query}, headers=headers)
            if request.status_code == 200:
                return request.json()
            else:
                raise Exception("Query failed to run by returning code of {}. {}".format(
                    request.status_code, query))
