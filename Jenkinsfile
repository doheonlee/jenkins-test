pipeline {
    agent {
        docker {
            image 'intovortex/python:3.9'
            label "local"
        }
    }

    triggers {
        GenericTrigger causeString: 'Github Webhook', genericVariables: [[defaultValue: '', key: 'GITHUB_ACTION', regexpFilter: '', value: '$.action'], [defaultValue: '', key: 'GITHUB_PROJECT', regexpFilter: '', value: '$.pull_request.base.repo.full_name'], [defaultValue: '', key: 'GITHUB_PR_NUMBER', regexpFilter: '', value: '$.pull_request.number']], token: 'jenkins-trigger'
}

    stages {
        stage('Approval Clearing') {
            when {
                expression { env.GITHUB_ACTION == "synchronize" }
            }
            environment {
                GITHUB_ACCESS_TOKEN = credentials("github-access-token")
            }
            steps {
                sh """
                    pwd
                    ls -alh
                    which python3.9
                    /usr/local/bin/python3.9 github_pr_checker.py --project ${env.GITHUB_PROJECT} --pr-num ${env.GITHUB_PR_NUMBER}
                """
            }
        }
    }
}

