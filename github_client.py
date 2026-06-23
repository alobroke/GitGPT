import json
import os
import requests


def load_event():

    event_path = os.environ.get(
        "GITHUB_EVENT_PATH"
    )

    if not event_path:
        return {}

    with open(
        event_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def extract_question(
    question_input
):

    if question_input:
        return question_input.strip()

    event = load_event()

    comment = (
        event.get("comment", {})
        .get("body", "")
    )

    if comment.startswith(
        "/gitgpt"
    ):

        return comment.replace(
            "/gitgpt",
            "",
            1
        ).strip()

    return ""


def post_comment(
    github_token,
    repo,
    answer,
    sources
):

    event = load_event()

    issue = event.get(
        "issue",
        {}
    )

    issue_number = issue.get(
        "number"
    )

    if not issue_number:
        return

    body = f"""
## GitGPT Answer

{answer}

### Sources

""" + "\n".join(
        f"- `{s}`"
        for s in sources
    )

    url = (
        f"https://api.github.com/repos/"
        f"{repo}/issues/"
        f"{issue_number}/comments"
    )

    requests.post(
        url,
        headers={
            "Authorization":
            f"Bearer {github_token}"
        },
        json={
            "body": body
        }
    )