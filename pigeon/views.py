from pigeon import app
from copy import deepcopy
import re
import requests
from flask import request
import json

JIRA_PROJECTS = app.config['JIRA_PROJECTS']
JIRA_URL = app.config['JIRA_URL']
USER = app.config['JIRA_USER']
PASS = app.config['JIRA_PASS']

ISSUE_COMMENT_URL = JIRA_URL + "/rest/api/2/issue/{issueIdOrKey}/comment"

COMMENT_TEMPLATE = """{author_name} referenced this issue in a commit.

{message}

{url}
"""

comment_json = {
    "body": None,
}


@app.route('/push', methods=["POST"])
def new_push():
    data = json.loads(request.data)

    for commit in data.get('commits', []):
        issues = get_message_issues(JIRA_PROJECTS, commit.get('message', ""))
        post_comment(data, commit, issues)

    return ""


def build_comment(data, commit):
    commit["author_name"] = commit["author"]["name"]
    commit["author_email"] = commit["author"]["email"]
    return COMMENT_TEMPLATE.format(**commit)


def post_comment(data, commit, issues):
    for issue in issues:
        existing_comments = get_existing_comments(issue)
        for comment_body in existing_comments:
            if commit['message'] in comment_body:
                print "skipping commit: %s" % commit
                return  # Don't post this commit as it (or one with the same message already has been posted)
        body = build_comment(data, commit)

        data = deepcopy(comment_json)
        data["body"] = body
        resp = requests.post(ISSUE_COMMENT_URL.format(issueIdOrKey=issue),
                             data=json.dumps(data),
                             auth=(USER, PASS),
                             headers={'content-type': 'application/json'})
        print resp
        # TODO: check response and email someone or something if it fails


def get_existing_comments(issue):
    r = requests.get(ISSUE_COMMENT_URL.format(issueIdOrKey=issue), auth=(USER, PASS))
    comment_list = r.json()['comments']
    return map(lambda c: c['body'], comment_list)


def get_message_issues(projects, msg):
    proj_search_str = "(?:"+"|".join(projects)+")"
    regex = "%s-[0-9]+" % proj_search_str
    return re.findall(regex, msg)
