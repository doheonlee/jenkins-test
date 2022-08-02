/*
 * PullRequest 의 webhook payload 를 parsing 하기 위해 GenericWebhookTrigger plugin 을 사용하였습니다.
 * Action(Event type), Project, PR Number 등은 payload 로 부터 JSONPath 로 Parsing하며,
 * Github interaction 을 위한 token 은 Jenkins Credential 을 사용하여 Environment Variable 로 전달하였습니다.
 *
 * Dismiss 를 skip 할 수 있는 Account 는 추후 변경 가능성을 위해, Job 의 Parameter 로 처리할 수 있도록
 * Multiline Text parameter 를 통해 입력받아, spaced string 으로 script 에 전달합니다.
 *
 * python 3.9 를 명시적으로 사용하기 위해, 빌드 환경이 Jenkins agent 에 독립적으로 구성되게끔
 * Containerized 로 구성하였습니다.
 */
pipeline {
    // Customized docker image has PyGithub, requests and argparse module
    agent {
        docker {
            image 'intovortex/python:3.9'
            label "local"
        }
    }

    // Generic Webhook Trigger starts this job with paylaod
    triggers {
        GenericTrigger(
            causeString: 'Github Webhook',
            genericVariables: [
                [defaultValue: '', key: 'GITHUB_ACTION', regexpFilter: '', value: '$.action'],
                [defaultValue: '', key: 'GITHUB_PROJECT', regexpFilter: '', value: '$.pull_request.base.repo.full_name'],
                [defaultValue: '', key: 'GITHUB_PR_NUMBER', regexpFilter: '', value: '$.pull_request.number']
            ],
            token: 'jenkins-trigger'
        )
    }

    // Accounts in SKIP_ACCOUNT don't dismissed even branch is updated
    parameters {
        text(
            name: 'SKIP_ACCOUNT',
            defaultValue: '''bot1
bot2 ''',
            description: 'This account approvals are not dismissed'
        )
    }


    stages {
        stage('Approval Clearing') {
            // Script is executed only branch update event(synchronize action)
            when {
                expression { env.GITHUB_ACTION == "synchronize" }
            }
            environment {
                GITHUB_ACCESS_TOKEN = credentials("github-access-token")
            }
            steps {
                script {
                    def skip_accounts = params.SKIP_ACCOUNT.replace("\n", " ")
                    sh """
                        /usr/local/bin/python3.9 github_pr_checker.py --project ${env.GITHUB_PROJECT} --pr-num ${env.GITHUB_PR_NUMBER} --accounts ${skip_accounts}
                """
                }
            }
        }
    }
}

