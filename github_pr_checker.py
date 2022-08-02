#!/usr/bin/env python3.9

import argparse

from github import Github

def initialize():
    parser = argparse.ArgumentParser(description="PullRequest approval checker")
    parser.add_argument("-p", "--project", action="store", type=str, required=True, help="Github Project")
    parser.add_argument("-n", "--pr-num", action="store", type=int, required=True, help="Github PullRequest Number")
    parser.add_argument("-a", "--account", action="append", type=str, help="Gitlab Account for skip clearing")

    parsed_args = parser.parse_args()
    print(parsed_args)

if __name__ == "__main__":
    initialize()
    g = Github("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")
    repo = g.get_repo("doheonlee/jenkins-test")
    pr = repo.get_pull(1)
    print(pr.get_reviews().totalCount)
    for review in pr.get_reviews():
        #review.dismiss("updated")
        # review.delete()
        print(review.state)
    pass
