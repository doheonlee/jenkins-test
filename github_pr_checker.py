#!/usr/bin/env python3.9

import argparse
import os

from github import Github

def parse_args():
    parser = argparse.ArgumentParser(description="PullRequest approval checker")
    parser.add_argument("-p", "--project",  action="store",  type=str, help="Github Project",            required=True)
    parser.add_argument("-n", "--pr-num",   action="store",  type=int, help="Github PullRequest Number", required=True)
    parser.add_argument("-a", "--accounts", action="extend", type=str, help="Github Accounts for skip clearing", nargs="+")

    return parser.parse_args()

def get_reviews(github_access_token, project, pr_num):
    github_client = Github(github_access_token)
    repo = github_client.get_repo(project)
    pr = repo.get_pull(pr_num)

    return pr.get_reviews()
    
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
    print(parsed_args)
    reviews = get_reviews(github_access_token, parsed_args.project, parsed_args.pr_num)
    print(f"Review count : {reviews.totalCount}")
    for review in reviews:
        #review.dismiss("updated")
        # review.delete()
        print(f"ID: {review.id}, USER_LOGIN: {review.user.login}, USER_NAME: {review.user.name}, STATE: {review.state}")
    pass
