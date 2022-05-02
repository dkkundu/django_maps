pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    environment {
        GH_SCRIPT = 'scripts/repo_status_update.sh'
        GH_OWNER = 'Tiger-Park-Limited'
        GH_REPO = 'DJMAPS'
        GH_TOKEN = credentials('TPL_Repo_Status')
        PROJ_NAME = "$GH_REPO"
        PROJ_DIR = "/opt/$GH_REPO"
        PROJ_ENV = "$PROJ_DIR/venv/bin"
    }

    stages {
        stage ('Status') {
            steps {
                echo 'Updating GitHub status...'
                sh "chmod 775 $GH_SCRIPT"
                sh "./$GH_SCRIPT pending $GH_OWNER $GH_REPO $GH_TOKEN $GIT_COMMIT $BUILD_URL"
            }
        }
        stage('Build') {
            steps {
                echo 'Building Docker container...'
                sh "mkdir -pv media/uploads && mkdir -pv logs && touch logs/debug.log"
                sh "cp -v examples/local_settings.example $PROJ_NAME/local_settings.py"
                sh 'docker-compose build'
            }
        }
        stage('Migrate') {
            steps {
                echo "Database migrations..."
                sh "docker-compose up -d db"
                sleep 5  // allow the db to startup and accept connections
                sh "docker-compose up -d"
                sh "chmod +x scripts/r-u-ready"
                sh "scripts/r-u-ready web -P 8000 -t 60"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing application...'
                // -T flag need to disable TTY input
                sh 'docker-compose exec -T app coverage run manage.py test'
                sh 'docker-compose exec -T app coverage xml -o coverage.xml'
                sh 'docker-compose exec -T app coverage report'
                sh 'docker-compose exec -T app flake8'
           }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying to test server...'
                sh """
                    ssh -v centos@pmfellowship.tiger-park.com \"
                        cd $PROJ_DIR && pwd
                        $PROJ_ENV/python -V
                        git --version && git pull
                        $PROJ_ENV/pip install -r requirements.txt
                        $PROJ_ENV/python manage.py wait_for_db
                        $PROJ_ENV/python manage.py migrate --noinput
                        $PROJ_ENV/python manage.py collectstatic --noinput
                        sudo systemctl restart djmaps
                        sudo systemctl status djmaps
                    \"
                """
            }
        }
    }

    post {
        always {
            cobertura coberturaReportFile: 'coverage.xml', enableNewApi: true
            sh 'docker-compose down'
        }
        success {
            sh "./$GH_SCRIPT success $GH_OWNER $GH_REPO $GH_TOKEN $GIT_COMMIT $BUILD_URL"
        }
        failure {
            sh "./$GH_SCRIPT failure $GH_OWNER $GH_REPO $GH_TOKEN $GIT_COMMIT $BUILD_URL"
        }
    }
}