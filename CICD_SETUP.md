# CI/CD Setup Guide

## Tổng quan flow

```
Developer push code
       │
       ▼
  GitHub / GitLab  ──webhook──►  Jenkins Master
                                      │
                                      ▼
                              Jenkins Agent
                          (Windows PC + USB Device)
                                      │
                            ┌─────────┴──────────┐
                            │  checkout code      │
                            │  pip install        │
                            │  pytest             │
                            │  archive reports    │
                            └─────────┬──────────┘
                                      │
                                      ▼
                            Jenkins Dashboard
                          HTML Report + JUnit trend
```

---

## Bước 1 — Cài Jenkins trên Windows PC có thiết bị

1. Tải Jenkins: https://www.jenkins.io/download/ → chọn **Windows**
2. Cài đặt → Jenkins chạy như Windows Service trên port 8080
3. Mở browser: `http://localhost:8080`
4. Làm theo wizard setup (cài "Suggested Plugins")

---

## Bước 2 — Cài Jenkins Plugins cần thiết

Vào **Manage Jenkins → Plugins → Available plugins**, cài:

| Plugin | Mục đích |
|--------|----------|
| **HTML Publisher** | Hiển thị HTML report trên Jenkins |
| **JUnit** | Hiển thị test trend chart (đã có sẵn) |
| **GitHub** | Nhận webhook từ GitHub |
| **Pipeline** | Chạy Jenkinsfile (đã có sẵn) |
| **Email Extension** | Gửi email thông báo (optional) |

---

## Bước 3 — Cấu hình Jenkins Agent (Windows PC)

Jenkins Master có thể chạy trên cùng máy (standalone) hoặc máy khác.
Nếu standalone, chỉ cần đặt label cho agent built-in:

**Manage Jenkins → Nodes → Built-In Node → Configure**
- Labels: `windows-dut`

Nếu Jenkins Master trên máy khác:
1. **Manage Jenkins → Nodes → New Node**
2. Điền tên, chọn **Permanent Agent**
3. Remote root directory: `C:\jenkins-agent`
4. Labels: `windows-dut`
5. Launch method: **Launch agent via Java Web Start** hoặc **SSH**

---

## Bước 4 — Tạo Pipeline Job

1. **New Item → Pipeline** → đặt tên `black-testing-framework`
2. **Pipeline section:**
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/yourname/black-testing-framework.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
3. **Save**

---

## Bước 5 — Cấu hình Webhook trên GitHub

1. Vào repo GitHub → **Settings → Webhooks → Add webhook**
2. Payload URL: `http://<jenkins-ip>:8080/github-webhook/`
3. Content type: `application/json`
4. Events: **Just the push event**
5. **Add webhook**

Từ đây, mỗi lần `git push` sẽ tự trigger Jenkins chạy tests.

---

## Bước 6 — Chạy thử

```
git add .
git commit -m "feat: add attenuator tests"
git push origin main
```

Jenkins tự động:
1. Checkout code mới
2. Cài dependencies vào virtualenv
3. Chạy pytest
4. Archive HTML + Excel report
5. Publish JUnit trend chart

---

## Cấu trúc report trên Jenkins

```
Jenkins Job
  ├── Test Result Trend  (JUnit chart qua các build)
  ├── Test Report        (HTML report — HTML Publisher)
  └── Build Artifacts
        ├── reports/html/report.html
        ├── reports/excel/test_results.xlsx
        └── reports/logs/pytest.log
```

---

## Chạy theo branch / môi trường

```groovy
// Trong Jenkinsfile — chạy smoke test trên PR, full test trên main
stage('Run Tests') {
    steps {
        script {
            def marker = env.BRANCH_NAME == 'main' ? '' : '-m smoke'
            bat "python -m pytest tests/ ${marker} ..."
        }
    }
}
```

---

## Environment variables trong Jenkins

Vào **Manage Jenkins → System → Global properties → Environment variables:**

| Name | Value |
|------|-------|
| `SERIAL_PORT` | `COM3` |
| `APP_EXE_PATH` | `C:\Apps\PC17\PC17.exe` |

Framework tự đọc các biến này — không cần sửa code.
