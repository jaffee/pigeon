from views import get_message_issues


def test_get_message_issues():
    projs = ["EKF", "AC"]
    ret = get_message_issues(projs, "well EKF-22 and [AC-3] but (EKF-999)")
    for iss in ["EKF-22", "AC-3", "EKF-999"]:
        assert iss in ret
