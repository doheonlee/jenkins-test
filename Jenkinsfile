pipeline {
    agent {
        docker {
            image "python:3.9"
        }
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

