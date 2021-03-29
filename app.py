# A Flask app set up using Githubs GraphQL API
import sys
#from gql_resolver import resolve
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from flask import Flask as fl

app = fl(__name__)

# github_auth = "Your Github PAT here"


headers = {"Authorization": github_auth}

#Gql setup
trnsprt = RequestsHTTPTransport(
    url="https://api.github.com/graphql", headers={"Authorization": github_auth},)

client = Client(
  transport=trnsprt
)

# Query to get a users list of repos
viewer_query = gql("""
query{
  viewer{
    login
    repositories(privacy: PUBLIC, first: 100, after: "BOUNDARY CURSOR") {
      edges {
        node {
          name
        }
      }
    }
  }
}
""")

repo_query = gql("""
query($repo:String!, $viewer:String!) { 
  repository(name: $repo, owner: $viewer) { 
    pushedAt
  }
}
""")

# Function to execute GraphQL queries
def resolve(query,**params):
  if len(params) > 0:
    return client.execute(query, variable_values=params)
  else:
    return client.execute(query)


# Function to get a string list of repository names for querying
def extract_repos_from_list(Lst):
    simplified_list = []
    for node in Lst:
        simplified_list.append(node['node']['name'])
    return simplified_list


def get_name_from_query(res):
    print(res)
    return res['viewer']['login']


def check_repo(Lst, viewer):
    dates_list = []
    for repo in Lst:
        params = {
            "repo": repo,
            "viewer": viewer
        }
        dates_list.append(resolve(repo_query, **params)['repository']['pushedAt'])
    return dates_list


@app.route('/')
def get_repos():
    result = resolve(viewer_query)  # Execute the query
    viewerName = get_name_from_query(result)
    repoList = result['viewer']['repositories']['edges']
    repoNames = extract_repos_from_list(repoList)
    datesList = check_repo(repoNames, viewerName)
    print(datesList)
    return "OK"


if __name__ == "___main___":
    app.run(debug=True)
