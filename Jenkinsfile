// ══════════════════════════════════════════════════════════════════════════
//  BLACK TESTING FRAMEWORK — Jenkins Declarative Pipeline
//
//  Flow: GitHub/GitLab push → Jenkins webhook → chạy trên Windows Agent
//        (agent là PC có cắm thiết bị USB)
//
//  Setup Jenkins agent:
//    - Label agent là "windows-dut"
//    - Agent phải là Windows machine có thiết bị cắm sẵn
//    - Cài Python + pip trên agent đó
// ══════════════════════════════════════════════════════════════════════════

pipeline {

    // Chạy trên Windows PC có thiết bị cắm — đặt label khi cấu hình agent
    agent { label 'windows-dut' }

    // ── Parameters — có thể chọn khi trigger manually ──────────────────────
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['demo', 'attenuator', 'all'],
            description: 'Chọn test suite cần chạy'
        )
        string(
            name: 'COM_PORT',
            defaultValue: 'COM3',
            description: 'COM port của thiết bị USB'
        )
        booleanParam(
            name: 'SKIP_HW_TESTS',
            defaultValue: false,
            description: 'Skip các test cần hardware (dùng khi chạy dry-run)'
        )
    }

    // ── Environment variables ───────────────────────────────────────────────
    environment {
        PYTHONDONTWRITEBYTECODE = '1'
        PYTHONUNBUFFERED        = '1'
        VENV_DIR                = '.venv'
        REPORT_DIR              = 'reports'
    }

    // ── Triggers — tự động chạy khi push lên GitHub/GitLab ─────────────────
    triggers {
        // Webhook từ GitHub/GitLab (cấu hình webhook trong repo settings)
        githubPush()
        // Hoặc poll SCM mỗi 5 phút (dùng khi không dùng webhook)
        // pollSCM('H/5 * * * *')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()               // không chạy song song (1 bộ hardware)
        timestamps()
    }

    // ════════════════════════════════════════════════════════════════════════
    //  STAGES
    // ════════════════════════════════════════════════════════════════════════

    stages {

        // ── 1. Checkout ────────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo "Branch: ${env.BRANCH_NAME} | Commit: ${env.GIT_COMMIT?.take(8)}"
                checkout scm
            }
        }

        // ── 2. Setup Python virtualenv ─────────────────────────────────────
        stage('Setup Environment') {
            steps {
                bat """
                    python -m venv ${env.VENV_DIR}
                    call ${env.VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        // ── 3. Tạo report directories ──────────────────────────────────────
        stage('Prepare Dirs') {
            steps {
                bat """
                    if not exist reports\\html      mkdir reports\\html
                    if not exist reports\\excel     mkdir reports\\excel
                    if not exist reports\\logs      mkdir reports\\logs
                    if not exist reports\\screenshots mkdir reports\\screenshots
                """
            }
        }

        // ── 4. Run Tests ───────────────────────────────────────────────────
        stage('Run Tests') {
            steps {
                script {
                    // Xác định thư mục test từ parameter
                    def testPath = 'tests/demo/'
                    if (params.TEST_SUITE == 'attenuator') {
                        testPath = 'tests/attenuator/'
                    } else if (params.TEST_SUITE == 'all') {
                        testPath = 'tests/'
                    }

                    // Build extra args
                    def extraArgs = ''
                    if (params.SKIP_HW_TESTS) {
                        extraArgs += ' -m "not hw_depend"'
                    }

                    // returnStatus=true → không throw exception khi test fail
                    // pytest exit code: 0=all pass, 1=some fail, 2=interrupted
                    def exitCode = bat(returnStatus: true, script: """
                        call ${env.VENV_DIR}\\Scripts\\activate.bat
                        set SERIAL_PORT=${params.COM_PORT}
                        python -m pytest ${testPath} ${extraArgs} ^
                            --junitxml=reports/junit.xml ^
                            --html=reports/html/report.html ^
                            --self-contained-html ^
                            -v
                    """)

                    // exit 0 = PASS, exit 1 = có test fail → UNSTABLE
                    // exit 2+ = pipeline lỗi thật sự → FAILURE
                    if (exitCode == 1) {
                        currentBuild.result = 'UNSTABLE'
                        echo "⚠️ Some tests FAILED — build marked UNSTABLE"
                    } else if (exitCode > 1) {
                        error("pytest crashed with exit code ${exitCode}")
                    }
                }
            }
        }
    }

    // ════════════════════════════════════════════════════════════════════════
    //  POST ACTIONS — luôn chạy dù pass hay fail
    // ════════════════════════════════════════════════════════════════════════

    post {

        always {
            // Publish JUnit XML → Jenkins hiển thị trend chart
            junit allowEmptyResults: true,
                  testResults: 'reports/junit.xml'

            // Archive toàn bộ reports
            archiveArtifacts artifacts: 'reports/**/*',
                             allowEmptyArchive: true,
                             fingerprint: true

            // Publish HTML report (cần plugin: HTML Publisher)
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
            echo "✅ ALL TESTS PASSED — Build #${env.BUILD_NUMBER}"
            // Gửi email / Slack khi pass (uncomment nếu đã cấu hình)
            // emailext subject: "✅ PASS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            //          body: "All tests passed.\n${env.BUILD_URL}",
            //          to: 'team@company.com'
        }

        failure {
            echo "❌ TEST FAILED — Build #${env.BUILD_NUMBER}"
            // emailext subject: "❌ FAIL: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            //          body: "Tests failed.\nSee: ${env.BUILD_URL}\n\nReport: ${env.BUILD_URL}Test_Report/",
            //          to: 'team@company.com'
        }

        unstable {
            echo "⚠️ BUILD UNSTABLE (some tests failed) — Build #${env.BUILD_NUMBER}"
        }
    }
}
