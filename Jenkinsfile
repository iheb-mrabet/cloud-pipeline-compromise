pipeline {
    agent any

    environment {
        IMAGE = "localhost:5000/vulnerable-flask-app:secure"
    }

    stages {
        stage('Integrity Check') {
            steps {
                sh '''
                cd /workspace
                if grep -E "kubectl[[:space:]]+exec|kubectl[[:space:]]+get[[:space:]]+secrets" Jenkinsfile | grep -v "grep"; then
                    echo "❌ Forbidden command detected"
                    exit 1
                fi
                echo "✅ Integrity OK"
                '''
            }
        }

        stage('Secret Scan') {
            steps {
                sh '''
                cd /workspace
                mkdir -p reports
                gitleaks detect --source app --no-git --report-format json --report-path reports/gitleaks.json
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                cd /workspace/app
                docker build -t $IMAGE .
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                docker push $IMAGE
                '''
            }
        }

        stage('Get Digest') {
            steps {
                script {
                    env.LOCAL_DIGEST = sh(
                        script: "docker inspect --format='{{index .RepoDigests 0}}' ${IMAGE}",
                        returnStdout: true
                    ).trim()

                    env.COSIGN_DIGEST = sh(
                        script: "echo ${LOCAL_DIGEST} | sed 's#localhost:5000#host.docker.internal:5000#'",
                        returnStdout: true
                    ).trim()

                    echo "LOCAL_DIGEST: ${LOCAL_DIGEST}"
                    echo "COSIGN_DIGEST: ${COSIGN_DIGEST}"
                }
            }
        }

        stage('HTTPS Registry Test') {
            steps {
                sh '''
                curl -k https://host.docker.internal:5000/v2/ || exit 1
                echo "✅ HTTPS registry reachable"
                '''
            }
        }

        stage('Sign Image') {
            steps {
                sh '''
                echo "Signing: $COSIGN_DIGEST"

                COSIGN_PASSWORD="24726739" cosign sign \
                  --key /var/jenkins_home/cosign.key \
                  --allow-insecure-registry=true \
                  --tlog-upload=false \
                  $COSIGN_DIGEST
                '''
            }
        }

        stage('Verify Signature') {
            steps {
                sh '''
                echo "Verifying: $COSIGN_DIGEST"

                cosign verify \
                  --key /var/jenkins_home/cosign.pub \
                  --allow-insecure-registry=true \
                  --insecure-ignore-tlog=true \
                  $COSIGN_DIGEST
                '''
            }
        }

        stage('Runtime Security Test') {
            steps {
                sh '''
                docker rm -f security-test || true
                docker run -d --name security-test $IMAGE
                sleep 3

                LOGS=$(docker logs security-test)

                if echo "$LOGS" | grep -Ei "\\[leak\\]|secret|token|password"; then
                    echo "❌ Runtime leak detected"
                    docker rm -f security-test
                    exit 1
                fi

                docker rm -f security-test
                echo "✅ Runtime safe"
                '''
            }
        }

        stage('Done') {
            steps {
                sh 'echo "🚀 HTTPS REGISTRY + COSIGN PIPELINE SECURED"'
            }
        }
    }
}
