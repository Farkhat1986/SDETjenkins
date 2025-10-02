pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'develop', url: 'https://github.com/Farkhat1986/SDETjenkins.git'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                script {
                    docker.image('python:3.10').inside {
                        sh '''
                            apt-get update -y
                            apt-get install -y python3-pip  # Установим pip, если он не установлен
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pytest --alluredir=allure-results
                        '''
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            junit '**/allure-results/*.xml'
            emailext(
                subject: "Python тесты — ${currentBuild.currentResult}",
                body: """
                    <h3>Сборка #${env.BUILD_NUMBER}</h3>
                    <p>Статус: <b>${currentBuild.currentResult}</b></p>
                    <p><a href="${env.BUILD_URL}allure-report">Смотреть Allure-отчёт</a></p>
                """,
                to: 'farhatsdet@mail.ru',
                mimeType: 'text/html'
            )
        }
    }
}

