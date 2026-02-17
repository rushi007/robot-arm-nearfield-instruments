#!groovy
pipeline {
    agent any
    options {
        timeout(time: 60, unit: 'MINUTES')       // Abort if > 60 mins
        disableConcurrentBuilds()                // Only 1 run at a time
        buildDiscarder(logRotator(numToKeepStr: '5')) // Keep last 5 builds
        timestamps()                             // Add timestamps to logs
    }
    environment {
        // Define any environment variables here
        // For example:
        // ARTIFACTORY_SERVER_ID = 'NearFieldInstruments'
        // ARTIFACTORY_BUILD_NAME = "nearfield-instruments/robot-arm"
    }}
    stages {
        stage('prepare') {
            steps {
                echo 'Preparing...'
                // Add preparation steps here, e.g. checkout code etc.
                // For example, to checkout code from Git:
                // git url: 'https://gitlab.com/your-repo.git', branch: 'main'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                # Add build steps here
                # For example, to build a Docker image:
                // sh 'docker build -t my-image:${env.BUILD_NUMBER} .'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                // Add test steps here, e.g. sh 'pytest' or similar
                // For example, to run tests with a shell command:
                // sh 'pytest tests/'
            }
        }
        stage('Post-build') {
            steps {
                echo 'Post-build actions...'
                // Add any post-build steps here, e.g. archiving artifacts, sending notifications, etc.
                // Push to GitLab, update commit status, etc.
                // For example, to update GitLab commit status:
                // updateGitlabCommitStatus name: '[Jenkins]', state: 'success'
            }
        }
    }
}
