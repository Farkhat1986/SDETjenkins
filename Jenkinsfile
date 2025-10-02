pipeline {
    agent {
        docker {
            image 'python:3.10' // Используем Python образ с установленным pip
            args '-v /tmp:/tmp' // Пример для монтирования временной папки, если нужно
        }
    }

    environment {
        // Устанавливаем переменные окружения для Allure
        ALLURE_RESULTS_DIR = 'allure-results'
        ALLURE_REPORT_DIR = 'allure-report'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'develop', url: 'https://github.com/Farkhat1986/SDETjenkins.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Проверим, установлен ли pip и необходимые пакеты
                    sh '''
                        # Проверка установки pip
                        if ! command -v pip &> /dev/null; then
                            echo "pip не найден, пожалуйста, установите его!"
                            exit 1
                        fi

                        # Установка зависимостей из requirements.txt
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install allure-pytest pytest
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Запуск тестов с выводом в директорию allure-results
                    sh '''
                        python -m pytest tests/ --alluredir=${ALLURE_RESULTS_DIR} --junitxml=test-results.xml -v
                    '''
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    // Генерация Allure-отчета
                    sh '''
                        allure generate ${ALLURE_RESULTS_DIR} -o ${ALLURE_REPORT_DIR} --clean
                    '''
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: "${ALLURE_RESULTS_DIR}"]]
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
                to: 'farhatsdet@mail.ru', // Уведомление на почту
                mimeType: 'text/html'
            )
        }

        success {
            // Успешное завершение сборки
            echo "Сборка прошла успешно!"
        }

        failure {
            // Ошибка сборки
            echo "Сборка завершена с ошибкой."
        }
    }
}
