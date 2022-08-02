#!/usr/bin/env python3.9

#
# Pull-Request 에 있는 Review 중, APPROVED 인 경우에만 해당 Review 를 Dismiss 하도록 구성되었습니다.
# Project, PullRequest Number, Account 를 매개변수로 입력받으며, 해당 프로젝트의 PullRequest 에서 삭제를 진행하며,
# Account 로 입력받은 ID 인 경우에는 Dismiss 하지 않습니다.
#

import argparse
import os
import sys

from github import Github
from github import GithubException

def parse_args():
    parser = argparse.ArgumentParser(description="PullRequest approval checker")
    parser.add_argument("-p", "--project",  action="store",  type=str, help="Github Project",            required=True)
    parser.add_argument("-n", "--pr-num",   action="store",  type=int, help="Github PullRequest Number", required=True)
    parser.add_argument("-a", "--accounts", action="extend", type=str, help="Github Accounts for skip dismissing", nargs="+")

    return parser.parse_args()

def get_reviews(github_access_token, project, pr_num):
    github_client = Github(github_access_token)
    repo = github_client.get_repo(project)
    pr = repo.get_pull(pr_num)

    return pr.get_reviews()
    
def get_approved_reviews(reviews, accounts):
    approved_reviews = []
    for review in reviews:
        if review.user.login in accounts:
            print(f"Skip dismissing {review.user.login}")
            continue
        if review.state == "APPROVED":
            approved_reviews.append(review)

    return approved_reviews

if __name__ == "__main__":
    # Get github access token from Jenkins credentials store
    # In order to hide this value from any logs, token is passed as GITHUB_ACCESS_TOKEN env value
    # If this value is not set, program will exit immediately with exit code 1
    github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not github_access_token:
        print("[ERROR] Invalid GITHUB_ACCESS_TOKEN, exit", file=sys.stderr)
        sys.exit(1)

    # Parse Github project, PR Number and reviewer account(s) from arguments
    parsed_args = parse_args()
    reviews = get_reviews(github_access_token, parsed_args.project, parsed_args.pr_num)
    approved_reviews = get_approved_reviews(reviews, parsed_args.accounts)

    # Dismiss approved reviews
    for review in approved_reviews:
        print(f"[DISMISS] ID: {review.id}, USER_LOGIN: {review.user.login}")
        try:
            review.dismiss("Branch is updated, existing approvals will be dismissed")
        except GithubException as e:
            print("[ERROR] Failed to dismiss review {review.id}", file=sys.stderr)
            print("[ERROR] " + str(e), file=sys.stderr)
    pass
