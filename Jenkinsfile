pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'github.com/Farkhat1986/SDETjenkins.git/'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                script {
                    docker.image('python:3.10').inside {
                        sh '''
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
            // Сохраняем JUnit результаты (если нужны для Jenkins)
            junit '**/allure-results/*.xml'

            // Отправляем письмо
            emailext(
                subject: "Python тесты — ${currentBuild.currentResult}",
                body: """
                    <h3>Сборка #${env.BUILD_NUMBER}</h3>
                    <p>Статус: <b>${currentBuild.currentResult}</b></p>
                    <p><a href="${env.BUILD_URL}allure">Смотреть Allure-отчёт</a></p>
                """,
                to: 'farhatsdet@mail.ru',
                mimeType: 'text/html'
            )
        }
    }
}

