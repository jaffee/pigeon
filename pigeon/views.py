from pigeon import app
import re
from flask import request
import json

JIRA_PROJECTS = app.config['JIRA_PROJECTS']
JIRA_URL = app.config['JIRA_URL']


@app.route('/push', methods=["POST"])
def new_push():
    data = json.loads(request.data)

    for commit in data.get('commits', []):
        issues = get_message_issues(JIRA_PROJECTS, commit.get('message', ""))
        commit["issues"] = issues

    return json.dumps(data)


def get_message_issues(projects, msg):
    proj_search_str = "(?:"+"|".join(projects)+")"
    regex = "%s-[0-9]+" % proj_search_str
    return re.findall(regex, msg)
