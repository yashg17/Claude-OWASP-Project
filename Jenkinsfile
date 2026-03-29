pipeline {
    agent any

    environment {
        // Ensure these IDs match what you saved in Jenkins -> Credentials
        CLAUDE_API_KEY = credentials('CLAUDE_API_KEY')
        SONAR_TOKEN       = credentials('SONAR_TOKEN')
        TARGET_FILE       = "app.py" // The file you want Claude to scan
    }

    stages {
        stage('Initialize') {
            steps {
                sh 'pip install anthropic python-dotenv --quiet'
                sh 'mkdir -p reports'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // 'SonarQube' must match Name in Jenkins -> Configure System
                withSonarQubeEnv('SonarQube') {
                    sh "sonar-scanner \
                        -Dsonar.projectKey=${JOB_NAME} \
                        -Dsonar.sources=. \
                        -Dsonar.login=${SONAR_TOKEN}"
                }
            }
        }

        stage('SonarQube Quality Gate') {
            steps {
                // This pauses the pipeline until SonarQube results are ready
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Claude AI Security Analysis') {
            steps {
                script {
                    // Runs the script; fails stage if exit code is 1 (CRITICAL found)
                    sh "python3 scripts/claude_review.py ${TARGET_FILE}"
                }
            }
        }
    }

    post {
        always {
            echo "==> Cleaning up Workspace..."
            cleanWs() 
        }
        success {
            echo "==> Pipeline Passed!"
        }
        failure {
            echo "==> Pipeline Failed. Check SonarQube or Claude Scan logs."
        }
    }
}
