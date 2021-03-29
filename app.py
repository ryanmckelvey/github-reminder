# A Flask app set up using Githubs GraphQL API
import requests
import sys
from flask import Flask as fl

app = fl(__name__)


github_auth = "Your Github PAT here"


headers = {"Authorization": github_auth}


# Query to get a users list of repos
query = """
{
  viewer{
    name
    repositories(privacy: PUBLIC, first: 100, after: "CURSOR OF BOUNDARY REPO==") {
      edges {
        node {
          name
        }
      }
    }
  }
}
"""


# Function to execute GraphQL queries
def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


# Function to get a string list of repository names for querying
def extract_repos_from_list(Lst):
    simplified_list = []
    for node in Lst:
        simplified_list.append(node['node']['name'])
    print(simplified_list, file=sys.stderr)
    return simplified_list


@app.route('/')
def get_repos():
    result = run_query(query)  # Execute the query
    repoList = result['data']['viewer']['repositories']['edges']
    repoNames = extract_repos_from_list(repoList)
    return "OK"


if __name__ == "___main___":
    app.run(debug=True)
