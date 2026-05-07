pipeline {

    // Máy A: Jenkins, PC17, S2VNA cùng 1 máy
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'signalgenerator', 'vna', 'power', 'spectrumanalyzer', 'amplifier', 'attenuator'],
            description: 'Module cần chạy: all = chạy tuần tự từng module'
        )
        string(
            name: 'TEST_CASE',
            defaultValue: '',
            description: 'Tên test case cụ thể (để trống = chạy cả module). VD: test_vna_puc_2_1_0007'
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
        SPIKE_EXE_PATH          = 'C:\\Program Files\\Signal Hound\\Spike\\Spike.exe'
    }

    options {
        timeout(time: 120, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        stage('Health Check Apps') {
            steps {
                script {
                    echo 'Health check S2VNA...'
                    bat "start \"\" \"${env.S2VNA_EXE_PATH}\""
                    bat 'ping -n 11 127.0.0.1 > nul'
                    def s2vnaOk = bat(returnStatus: true, script: 'tasklist /fi "imagename eq S2VNA.exe" | findstr /i S2VNA.exe > nul 2>&1')
                    if (s2vnaOk != 0) error('S2VNA không khởi động được — dừng pipeline')
                    echo 'S2VNA OK'

                    echo 'Health check PC17...'
                    bat "start \"\" \"${env.APP_EXE_PATH}\""
                    def pc17Ok = false
                    for (int i = 0; i < 12; i++) {
                        bat 'ping -n 6 127.0.0.1 > nul'
                        def rc = bat(returnStatus: true, script: 'tasklist /fi "imagename eq PC17.exe" | findstr /i PC17.exe > nul 2>&1')
                        if (rc == 0) { pc17Ok = true; break }
                        echo "PC17 chưa sẵn sàng — thử lại (${i+1}/12)..."
                    }
                    if (!pc17Ok) error('PC17 không khởi động được sau 60s — dừng pipeline')
                    echo 'PC17 OK'

                    echo 'Đóng tất cả app sau health check...'
                    bat(returnStatus: true, script: 'taskkill /f /im S2VNA.exe 2>nul')
                    bat(returnStatus: true, script: 'taskkill /f /im PC17.exe  2>nul')
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
                    def markerArgs = params.SKIP_HW_TESTS ? '-m "not hw_depend"' : ''
                    def filterArgs = params.TEST_CASE?.trim() ? "-k \"${params.TEST_CASE}\"" : ''
                    def extraArgs  = [filterArgs, markerArgs].findAll { it }.join(' ')

                    if (params.TEST_SUITE == 'all') {
                        // ── Chạy tuần tự từng module theo thứ tự rõ ràng ──────────────
                        def modules = ['signalgenerator', 'power', 'amplifier', 'attenuator', 'spectrumanalyzer', 'vna']
                        def maxExitCode = 0

                        for (int i = 0; i < modules.size(); i++) {
                            def module = modules[i]
                            echo "======================================================"
                            echo "  Module ${i+1}/${modules.size()}: ${module.toUpperCase()}"
                            echo "======================================================"

                            // Launch app cần thiết trước module tương ứng
                            if (module == 'spectrumanalyzer') {
                                echo 'Khởi động Spike trước Spectrum module...'
                                bat "start \"\" \"${env.SPIKE_EXE_PATH}\""
                                bat 'ping -n 11 127.0.0.1 > nul'
                                def spRc = bat(returnStatus: true, script: 'tasklist /fi "imagename eq Spike.exe" | findstr /i Spike.exe > nul 2>&1')
                                if (spRc != 0) {
                                    echo 'WARNING: Spike không khởi động — bỏ qua Spectrum module'
                                    continue
                                }
                                echo 'Spike sẵn sàng'
                            }

                            if (module == 'vna') {
                                echo 'Khởi động S2VNA trước VNA module...'
                                bat "start \"\" \"${env.S2VNA_EXE_PATH}\""
                                bat 'ping -n 11 127.0.0.1 > nul'
                                def s2rc = bat(returnStatus: true, script: 'tasklist /fi "imagename eq S2VNA.exe" | findstr /i S2VNA.exe > nul 2>&1')
                                if (s2rc != 0) {
                                    echo 'WARNING: S2VNA không khởi động — bỏ qua VNA module'
                                    continue
                                }
                                echo 'S2VNA sẵn sàng'
                            }

                            def rc = bat(returnStatus: true, script: """
                                call ${env.VENV_DIR}\\Scripts\\activate.bat
                                set SERIAL_PORT=${params.COM_PORT}
                                set TEST_SUITE=${module}
                                python -m pytest tests/${module}/ ${extraArgs} -v ^
                                    --html=reports/html/${module}_report.html ^
                                    --junitxml=reports/junit_${module}.xml
                            """)

                            if (rc > maxExitCode) maxExitCode = rc
                            echo "Module ${module} xong — exit code: ${rc}"

                            // Kill tất cả app sau mỗi module → môi trường sạch
                            bat(returnStatus: true, script: 'taskkill /f /im PC17.exe  2>nul')
                            bat(returnStatus: true, script: 'taskkill /f /im S2VNA.exe 2>nul')
                            bat(returnStatus: true, script: 'taskkill /f /im Spike.exe 2>nul')
                            bat 'ping -n 4 127.0.0.1 > nul'
                        }

                        env.PYTEST_EXIT_CODE = "${maxExitCode}"

                        // Gộp tất cả module Excel → all_report.xlsx
                        echo 'Generating all_report.xlsx...'
                        bat """
                            call ${env.VENV_DIR}\\Scripts\\activate.bat
                            python scripts/merge_excel_reports.py
                        """

                        if (maxExitCode >= 2) {
                            error("Một hoặc nhiều module bị lỗi hệ thống (max exit code ${maxExitCode})")
                        }

                    } else {
                        // ── Chạy 1 module cụ thể ──────────────────────────────────────
                        echo "======================================================"
                        echo "  Module: ${params.TEST_SUITE.toUpperCase()}"
                        echo "======================================================"

                        // Launch app cần thiết trước module tương ứng
                        if (params.TEST_SUITE == 'spectrumanalyzer') {
                            echo 'Khởi động Spike trước Spectrum module...'
                            bat "start \"\" \"${env.SPIKE_EXE_PATH}\""
                            bat 'ping -n 11 127.0.0.1 > nul'
                            def spRc = bat(returnStatus: true, script: 'tasklist /fi "imagename eq Spike.exe" | findstr /i Spike.exe > nul 2>&1')
                            if (spRc != 0) error('Spike không khởi động được — dừng pipeline')
                            echo 'Spike sẵn sàng'
                        }

                        if (params.TEST_SUITE == 'vna') {
                            echo 'Khởi động S2VNA trước VNA module...'
                            bat "start \"\" \"${env.S2VNA_EXE_PATH}\""
                            bat 'ping -n 11 127.0.0.1 > nul'
                            def s2rc = bat(returnStatus: true, script: 'tasklist /fi "imagename eq S2VNA.exe" | findstr /i S2VNA.exe > nul 2>&1')
                            if (s2rc != 0) error('S2VNA không khởi động được — dừng pipeline')
                            echo 'S2VNA sẵn sàng'
                        }

                        def testPath = "tests/${params.TEST_SUITE}/"
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
    }

    post {
        always {
            // Thu thập JUnit: module riêng (all) hoặc file chung (single module)
            junit allowEmptyResults: true, testResults: 'reports/junit*.xml'

            archiveArtifacts artifacts: 'reports/**/*',
                             allowEmptyArchive: true

            publishHTML(target: [
                allowMissing         : true,
                alwaysLinkToLastBuild: true,
                keepAll              : true,
                reportDir            : 'reports/html',
                reportFiles          : 'report.html,*_report.html',
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
            bat(returnStatus: true, script: 'taskkill /f /im S2VNA.exe 2>nul')
            bat(returnStatus: true, script: 'taskkill /f /im PC17.exe  2>nul')
            bat(returnStatus: true, script: 'taskkill /f /im Spike.exe 2>nul')
        }
    }
}
