from views import get_message_issues, commit_msg_from_comment, substantially_similar, log
from nose.tools import assert_equals


def test_get_message_issues():
    projs = ["EKF", "AC"]
    ret = get_message_issues(projs, "well EKF-22 and [AC-3] but (EKF-999)")
    for iss in ["EKF-22", "AC-3", "EKF-999"]:
        assert iss in ret


def test_commit_msg_from_comment():
    comment = 'Matthew King just referenced this issue in a commit.\n\n[WWW-93] updated www, el and engineering umbel-ui in bower to ^1.0.0\n\nhttps://gitlab.umbel.com/el-umbel/umbel/commit/9d0abfc1d105d209c825ccdfecff7bed97845049\n'

    actual = commit_msg_from_comment(comment)
    expected = "[WWW-93] updated www, el and engineering umbel-ui in bower to ^1.0.0"

    assert_equals(actual, expected)


def test_substatially_similar():
    assert substantially_similar("asdfghjkl", "asdfghjkl")
    assert substantially_similar("asdfghjkzlppp", "asdfghjkzlppq")
    assert not substantially_similar("hello", "goodbye")


def test_log():
    log("hello")
