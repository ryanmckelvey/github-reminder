# A Flask app set up using Githubs GraphQL API and SMTPLib
import sys
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from flask import Flask as fl
from email_service import emailService


app = fl(__name__)

github_auth = "AUTH TOKEN HERE"
# github_auth = "Your Github PAT here"


headers = {"Authorization": github_auth}

# Gql setup
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
    repositories(privacy: PUBLIC, first: 100, after: "BOUNDARY CURSOR HERE") {
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

# Instantiating Email Service client
em = emailService()

# Function to execute GraphQL queries


def resolve(query, **params):
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

# Function to return list of datetimes of the last push of each repo from repoList.


def check_repo(Lst, viewer):
    dates_list = []
    for repo in Lst:
        params = {
            "repo": repo,
            "viewer": viewer
        }
        # Add the results of the gql repo_query resolution to a list.
        dates_list.append(resolve(repo_query, **params)
                          ['repository']['pushedAt'])
    return latest_pushedAt(dates_list)


def latest_pushedAt(dates):
    date_time_str = max(dates)
    date_time_obj = datetime.datetime.strptime(date_time_str.split('T')[0], '%Y-%m-%d')
    return date_time_obj.date()

# Function for compiling email body and sending email.


def email_send(viewer, date):
    message = """\
    Subject: Hey {}

    Your last push was on {}, get to work!!
  """.format(viewer,date)
    em.send_email(message)


@app.route('/')
def main_method():
    result = resolve(viewer_query)  # Execute the viewer query
    viewerName = result['viewer']['login']
    repoList = result['viewer']['repositories']['edges']
    repoNames = extract_repos_from_list(repoList)
    latestPushedAt = check_repo(repoNames, viewerName)
    print("Email send is hanging")
    email_send(viewerName, latestPushedAt)
    return "OK"


if __name__ == "___main___":
    app.run(debug=True)
