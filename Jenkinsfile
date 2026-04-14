pipeline {

    // Máy A: Jenkins, PC17, S2VNA cùng 1 máy
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['vna', 'attenuator', 'all'],
            description: 'Chọn bộ test cần chạy'
        )
        string(
            name: 'COM_PORT',
            defaultValue: 'COM3',
            description: 'COM port của thiết bị USB'
        )
        booleanParam(
            name: 'SKIP_HW_TESTS',
            defaultValue: false,
            description: 'Bỏ qua test cần hardware (dry-run)'
        )
    }

    environment {
        PYTHONDONTWRITEBYTECODE = '1'
        PYTHONUNBUFFERED        = '1'
        VENV_DIR                = '.venv'
        APP_EXE_PATH            = 'C:\\PC17\\PC17.exe'
        S2VNA_EXE_PATH          = 'C:\\S2VNA\\S2VNA.exe'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat """
                    python -m venv ${env.VENV_DIR}
                    call ${env.VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip --quiet
                    pip install -r requirements.txt --quiet
                """
            }
        }

        stage('Prepare Dirs') {
            steps {
                bat """
                    if not exist reports\\html        mkdir reports\\html
                    if not exist reports\\excel       mkdir reports\\excel
                    if not exist reports\\logs        mkdir reports\\logs
                    if not exist reports\\screenshots mkdir reports\\screenshots
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def testPath
                    switch(params.TEST_SUITE) {
                        case 'vna':        testPath = 'tests/vna/';        break
                        case 'attenuator': testPath = 'tests/attenuator/'; break
                        default:           testPath = 'tests/'
                    }

                    def extraArgs = params.SKIP_HW_TESTS ? '-m "not hw_depend"' : ''

                    def exitCode = bat(returnStatus: true, script: """
                        call ${env.VENV_DIR}\\Scripts\\activate.bat
                        set SERIAL_PORT=${params.COM_PORT}
                        python -m pytest ${testPath} ${extraArgs} -v
                    """)

                    env.PYTEST_EXIT_CODE = "${exitCode}"

                    if (exitCode >= 2) {
                        error("pytest bị lỗi hệ thống (exit code ${exitCode})")
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'

            archiveArtifacts artifacts: 'reports/**/*',
                             allowEmptyArchive: true

            publishHTML(target: [
                allowMissing         : true,
                alwaysLinkToLastBuild: true,
                keepAll              : true,
                reportDir            : 'reports/html',
                reportFiles          : 'report.html',
                reportName           : 'Test Report'
            ])
        }

        success {
            script {
                def code = env.PYTEST_EXIT_CODE?.toInteger() ?: 0
                if (code == 0) {
                    echo "ALL TESTS PASSED"
                } else {
                    echo "BUILD OK — nhưng có test FAILED, xem Test Report"
                }
            }
        }

        failure {
            echo "PIPELINE FAILED — xem Console Output để biết lý do"
        }
    }
}
