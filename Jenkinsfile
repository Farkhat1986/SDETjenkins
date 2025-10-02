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
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install allure-pytest  # Установим allure-pytest
                            curl -o allure-2.13.8.tgz -L https://github.com/allure-framework/allure2/releases/download/2.13.8/allure-2.13.8.tgz  # Скачиваем allure
                            tar -zxvf allure-2.13.8.tgz -C /opt/  # Разархивируем
                            export PATH=$PATH:/opt/allure-2.13.8/bin  # Добавляем в PATH
                            pytest --alluredir=allure-results  # Запуск тестов с результатами в allure-results
                        '''
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]  // Генерация отчета
            }
        }
    }

    post {
        always {
            junit '**/allure-results/*.xml'  // Используем junit для Jenkins
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
