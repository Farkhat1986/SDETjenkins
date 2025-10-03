pipeline {
    agent {
        docker {
            image 'python:3.11'   // Контейнер с Python
            args '-v /var/run/docker.sock:/var/run/docker.sock -v $WORKSPACE:/workspace -w /workspace'
        }
    }

    environment {
        ALLURE_RESULTS_DIR = 'allure-results'
        ALLURE_REPORT_DIR  = 'allure-report'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'develop', url: 'https://github.com/Farkhat1986/SDETjenkins.git'
            }
        }

        stage('Start environment') {
            steps {
                sh '''
                    echo "Запускаем WordPress + MySQL через docker-compose..."
                    docker-compose -f docker-compose.yml up -d
                    echo "Ждём, пока сервисы поднимутся..."
                    sleep 20
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest allure-pytest
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    pytest tests/ \
                        --junitxml=junit-report.xml \
                        --alluredir=${ALLURE_RESULTS_DIR} -v
                '''
            }
        }

        stage('Generate Allure report') {
            steps {
                sh '''
                    allure generate ${ALLURE_RESULTS_DIR} -o ${ALLURE_REPORT_DIR} --clean
                '''
            }
        }

        stage('Publish reports') {
            steps {
                junit 'junit-report.xml'
                allure includeProperties: false, jdk: '', results: [[path: "${ALLURE_RESULTS_DIR}"]]
            }
        }
    }

    post {
        always {
            sh '''
                echo "Останавливаем docker-compose окружение..."
                docker-compose -f docker-compose.yml down
            '''
            emailext(
                subject: "Python тесты — ${currentBuild.currentResult}",
                body: """
                    <h3>Сборка #${env.BUILD_NUMBER}</h3>
                    <p>Статус: <b>${currentBuild.currentResult}</b></p>
                    <p><a href="${env.BUILD_URL}allure-report">Allure-отчёт</a></p>
                """,
                to: 'farhatsdet@mail.ru',
                mimeType: 'text/html'
            )
        }
    }
}
