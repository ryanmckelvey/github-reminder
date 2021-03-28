# A Flask app set up using Githubs GraphQL API
import requests
from flask import Flask as fl

app = fl(__name__)

#github_auth = "Your Github PAT here"

headers = {"Authorization": github_auth}

query = """
{
  user(login: "YOUR LOGIN") {
    name
    repositories(privacy: PUBLIC, first: 100, after: "CURSOR") {
      edges {
        node {
          name
        }
      }
    }
  }
}
"""

##Function to execute GraphQL queries
def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


@app.route('/')
def get_repos():
    result = run_query(query)  # Execute the query
    return result
