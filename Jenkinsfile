pipeline {

    // Máy A: Jenkins, PC17, S2VNA cùng 1 máy
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'vna', 'power', 'spectrumanalyzer', 'amplifier', 'attenuator'],
            description: 'Module cần chạy: all | vna | power | spectrumanalyzer | amplifier | attenuator'
        )
        string(
            name: 'TEST_CASE',
            defaultValue: '',
            description: 'Tên test case cụ thể (để trống = chạy cả module). VD: test_vna_puc_2_1_normal'
        )
        string(
            name: 'GIT_COMMIT_ID',
            defaultValue: '',
            description: 'Commit SHA muốn chạy (để trống = HEAD của nhánh). VD: abc1234'
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
        APP_EXE_PATH            = 'C:\\EliteRF\\PC17.exe'
        S2VNA_EXE_PATH          = 'C:\\VNA\\S2VNA\\S2VNA.exe'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        stage('Health Check Apps') {
            steps {
                script {
                    // Mở từng app, xác nhận đang chạy, rồi đóng hết
                    // Test case sẽ tự mở lại khi cần

                    echo 'Health check S2VNA...'
                    bat "start \"\" \"${env.S2VNA_EXE_PATH}\""
                    bat 'ping -n 11 127.0.0.1 > nul'
                    def s2vnaOk = bat(returnStatus: true, script: 'tasklist /fi "imagename eq S2VNA.exe" | findstr /i S2VNA.exe > nul 2>&1')
                    if (s2vnaOk != 0) error('S2VNA không khởi động được — dừng pipeline')
                    echo 'S2VNA OK'

                    echo 'Health check PC17...'
                    bat "start \"\" \"${env.APP_EXE_PATH}\""
                    // Retry mỗi 5s, tối đa 60s — PC17 khởi động chậm hơn S2VNA
                    def pc17Ok = false
                    for (int i = 0; i < 12; i++) {
                        bat 'ping -n 6 127.0.0.1 > nul'
                        def rc = bat(returnStatus: true, script: 'tasklist /fi "imagename eq PC17.exe" | findstr /i PC17.exe > nul 2>&1')
                        if (rc == 0) { pc17Ok = true; break }
                        echo "PC17 chưa sẵn sàng — thử lại (${i+1}/12)..."
                    }
                    if (!pc17Ok) error('PC17 không khởi động được sau 60s — dừng pipeline')
                    echo 'PC17 OK'

                    // Đóng hết — test case tự mở lại
                    echo 'Đóng tất cả app trước khi chạy test...'
                    bat(returnStatus: true, script: 'taskkill /f /im S2VNA.exe 2>nul')
                    bat(returnStatus: true, script: 'taskkill /f /im PC17.exe  2>nul')
                    bat(returnStatus: true, script: 'taskkill /f /im Spike.exe 2>nul')
                    bat 'ping -n 3 127.0.0.1 > nul'
                    echo 'Health check hoàn tất — sẵn sàng chạy test'
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    if (params.GIT_COMMIT_ID?.trim()) {
                        echo "Checking out specific commit: ${params.GIT_COMMIT_ID}"
                        bat "git checkout ${params.GIT_COMMIT_ID}"
                    } else {
                        echo "Using HEAD commit: ${bat(returnStdout: true, script: 'git rev-parse --short HEAD').trim()}"
                    }
                }
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
                        case 'vna':              testPath = 'tests/vna/';             break
                        case 'power':            testPath = 'tests/power/';           break
                        case 'spectrumanalyzer': testPath = 'tests/spectrumanalyzer/'; break
                        case 'amplifier':        testPath = 'tests/amplifier/';       break
                        case 'attenuator':       testPath = 'tests/attenuator/';      break
                        default:                 testPath = 'tests/'
                    }

                    // Nếu TEST_CASE được điền → chạy đúng test case đó (dùng -k)
                    def filterArgs = params.TEST_CASE?.trim() ? "-k \"${params.TEST_CASE}\"" : ''
                    def markerArgs = params.SKIP_HW_TESTS ? '-m "not hw_depend"' : ''
                    def extraArgs  = [filterArgs, markerArgs].findAll { it }.join(' ')

                    echo "Running: pytest ${testPath} ${extraArgs}"

                    def exitCode = bat(returnStatus: true, script: """
                        call ${env.VENV_DIR}\\Scripts\\activate.bat
                        set SERIAL_PORT=${params.COM_PORT}
                        set TEST_SUITE=${params.TEST_SUITE}
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

        cleanup {
            // Tắt tất cả app sau mỗi build (pass hay fail)
            bat(returnStatus: true, script: 'taskkill /f /im S2VNA.exe 2>nul')
            bat(returnStatus: true, script: 'taskkill /f /im PC17.exe  2>nul')
            bat(returnStatus: true, script: 'taskkill /f /im Spike.exe 2>nul')
        }
    }
}
