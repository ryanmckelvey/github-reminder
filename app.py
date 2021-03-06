# A Flask app set up using Githubs GraphQL API and SMTPLib
import sys
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from flask import Flask as fl
from flask import request
from email_service import emailService


app = fl(__name__)


github_auth = "Bearer YOUR GIT PAT HERE"

auth = "auth_param"
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
    repositories(privacy: PUBLIC, first: 100) {
      edges {
        node {
          name
          owner{
            login
          }
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
def extract_repos_from_list(Lst,viewer):
    simplified_list = []
    for node in Lst:
      if node['node']['owner']['login'] == viewer:
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


def email_send(viewer, dte):
    message = """\
    Hey {}\n\n
    GitHub Reminder

    Your last push was on {}, get to work!!
  """.format(viewer,dte)
    if dte < datetime.date.today():
      em.send_email(message)


@app.route('/')
def main_function():
    if(request.args.get('key') == auth):
      result = resolve(viewer_query)  # Execute the viewer query
      viewerName = result['viewer']['login']
      repoList = result['viewer']['repositories']['edges']
      repoNames = extract_repos_from_list(repoList,viewerName)
      latestPushedAt = check_repo(repoNames, viewerName)
      email_send(viewerName, latestPushedAt)
      return "OK"
    else:
      return "invalid"
