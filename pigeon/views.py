from pigeon import app
from copy import deepcopy
import re
import requests
from flask import request
import json
import Levenshtein
from datetime import datetime

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


def log(s):
    t = datetime.now().isoformat()
    print "%s, %s" % (t, s)


@app.route('/push', methods=["POST"])
def new_push():
    data = json.loads(request.data)

    for commit in data.get('commits', []):
        # skip merge commits
        if commit.get('message', "").startswith('Merge branch'):
            continue
        issues = set(get_message_issues(JIRA_PROJECTS, commit.get('message', "")))
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
            msg = commit_msg_from_comment(comment_body)
            if substantially_similar(msg, commit['message']):
                log("skipping commit: %s" % commit)
                return  # Don't post this commit as it (or one with the same message already has been posted)
        body = build_comment(data, commit)

        data = deepcopy(comment_json)
        data["body"] = body
        r = requests.post(ISSUE_COMMENT_URL.format(issueIdOrKey=issue),
                          data=json.dumps(data),
                          auth=(USER, PASS),
                          headers={'content-type': 'application/json'})
        log("Posted commit status:%s, issue:%s, message: %s" % (r.status_code, issue, commit["message"]))
        # TODO: check response and email someone or something if it fails


def commit_msg_from_comment(comment):
    beg_ind = comment.index("\n\n") + 2
    end_ind = comment.rindex("\n\n")
    return comment[beg_ind:end_ind]


def substantially_similar(s1, s2):
    d = Levenshtein.distance(s1, s2)
    sim = float(d) / float(max(len(s1), len(s2)))
    if sim < 0.1:
        return True
    else:
        return False


def get_existing_comments(issue):
    r = requests.get(ISSUE_COMMENT_URL.format(issueIdOrKey=issue), auth=(USER, PASS))
    if r.status_code < 200 or r.status_code >= 300:
        raise APIError(r)
    comment_list = r.json()['comments']
    return map(lambda c: c['body'], comment_list)


def get_message_issues(projects, msg):
    proj_search_str = "(?:" + "|".join(projects) + ")"
    regex = "%s-[0-9]+" % proj_search_str
    return re.findall(regex, msg)


class APIError(Exception):
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        r = self.resp
        return "Got a non-OK response %s - r:\n  %s" % (r.status_code, r.content)
