# Hướng dẫn cài đặt CI/CD — Black Testing Framework

## Mục lục
1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Cài đặt Jenkins (Interactive Mode)](#2-cài-đặt-jenkins-interactive-mode)
3. [Cài đặt Task Scheduler cho App Launch](#3-cài-đặt-task-scheduler-cho-app-launch)
4. [Cấu hình Jenkins Pipeline](#4-cấu-hình-jenkins-pipeline)
5. [Chạy Test lần đầu](#5-chạy-test-lần-đầu)
6. [Tham số Pipeline](#6-tham-số-pipeline)
7. [Xử lý lỗi thường gặp](#7-xử-lý-lỗi-thường-gặp)

---

## 1. Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|---|---|
| OS | Windows 10 (đã test trên 10.0.19045) |
| Python | 3.10 – 3.12 (khuyến nghị), tránh 3.14 nếu gặp COM crash |
| Java | JDK 11+ (đã dùng Eclipse Adoptium JDK 25) |
| Jenkins | 2.x (file `.war`) |
| Git | Đã cài và có thể dùng từ CMD |
| App | PC17.exe đã cài tại `C:\PC17\` |
| App | S2VNA.exe đã cài tại `C:\VNA\S2VNA\` |

---

## 2. Cài đặt Jenkins (Interactive Mode)

> **Quan trọng:** pywinauto cần chạy trong **interactive desktop session** của user đang login.
> Jenkins Service chạy trong Session 0 (non-interactive) sẽ KHÔNG thể điều khiển GUI app.
> Giải pháp: chạy Jenkins như một **process thường** trong session của user.

### Bước 2.1 — Disable Jenkins Service (nếu đã cài)

Mở CMD với quyền **Administrator**:

```cmd
net stop jenkins
sc config jenkins start= disabled
```

### Bước 2.2 — Tạo Task Scheduler để auto-start Jenkins khi login

Thay `<YOUR_USERNAME>` bằng kết quả của lệnh `whoami`:

```cmd
schtasks /create /tn "JenkinsStartup" ^
  /tr "\"C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin\java.exe\" -DJENKINS_HOME=\"C:\ProgramData\Jenkins\.jenkins\" -jar \"C:\Program Files\Jenkins\Jenkins.war\" --httpPort=8080" ^
  /sc onlogon ^
  /ru "<DOMAIN>\<YOUR_USERNAME>" ^
  /it /f
```

> `/it` = interactive — bắt buộc để Jenkins chạy trong desktop session của user

### Bước 2.3 — Khởi động Jenkins ngay (không cần restart máy)

```cmd
schtasks /run /tn "JenkinsStartup"
```

Đợi ~30 giây rồi vào `http://localhost:8080`.

### Bước 2.4 — Lấy Initial Admin Password (lần đầu)

```cmd
type "C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword"
```

Paste vào trang setup Jenkins → Install suggested plugins → tạo admin user.

---

## 3. Cài đặt Task Scheduler cho App Launch

pywinauto cần launch app trong **interactive session**. Dùng Task Scheduler với flag `/it`.

Mở CMD với quyền **Administrator**, thay `<DOMAIN>\<YOUR_USERNAME>` cho đúng:

```cmd
schtasks /create /tn "CI_LaunchS2VNA" ^
  /tr "C:\VNA\S2VNA\S2VNA.exe" ^
  /sc once /st 00:00 ^
  /ru "<DOMAIN>\<YOUR_USERNAME>" ^
  /it /f

schtasks /create /tn "CI_LaunchPC17" ^
  /tr "C:\PC17\PC17.exe" ^
  /sc once /st 00:00 ^
  /ru "<DOMAIN>\<YOUR_USERNAME>" ^
  /it /f
```

Kiểm tra đã tạo thành công:

```cmd
schtasks /query /tn "CI_LaunchS2VNA"
schtasks /query /tn "CI_LaunchPC17"
```

> **Lưu ý:** User phải **đang login** vào Windows khi Jenkins build chạy. Task với `/it` chỉ hoạt động khi có interactive session đang mở.

---

## 4. Cấu hình Jenkins Pipeline

### Bước 4.1 — Tạo Pipeline Job

1. Vào `http://localhost:8080` → **New Item**
2. Nhập tên: `PC17-Tests` → chọn **Pipeline** → OK
3. Tab **Pipeline** → chọn **Pipeline script from SCM**
4. SCM: **Git** → nhập URL repo
5. Branch: `*/main`
6. Script Path: `Jenkinsfile`
7. **Save**

### Bước 4.2 — Cấu hình Git Credentials (nếu repo private)

1. **Manage Jenkins** → **Credentials** → **Add Credentials**
2. Kind: **Username with password** hoặc **SSH Username with private key**
3. Nhập thông tin GitHub → Save

---

## 5. Chạy Test lần đầu

### Checklist trước khi chạy

- [ ] User đang login vào Windows (không lock screen)
- [ ] Jenkins đang chạy tại `http://localhost:8080`
- [ ] Task Scheduler `CI_LaunchS2VNA` và `CI_LaunchPC17` đã được tạo
- [ ] Code đã được push lên GitHub

### Trigger build

1. Vào `http://localhost:8080/job/PC17-Tests`
2. Click **Build with Parameters** (cột trái)
3. Điền tham số (xem mục 6)
4. Click **Build**
5. Click vào build đang chạy → **Console Output** để xem log real-time

---

## 6. Tham số Pipeline

| Tham số | Mặc định | Mô tả |
|---|---|---|
| `TEST_SUITE` | `vna` | Module cần chạy: `vna` / `attenuator` / `demo` / `all` |
| `TEST_CASE` | _(trống)_ | Tên test function cụ thể, VD: `test_vna_puc_2_1_0001`. Để trống = chạy cả module |
| `GIT_COMMIT_ID` | _(trống)_ | SHA commit muốn test, VD: `abc1234`. Để trống = dùng HEAD |
| `COM_PORT` | `COM3` | COM port của thiết bị USB |
| `SKIP_HW_TESTS` | `false` | Tick để bỏ qua test cần hardware (dry-run) |

### Ví dụ thực tế

**Chạy 1 test case cụ thể:**
- `TEST_SUITE = vna`
- `TEST_CASE = test_vna_puc_2_1_0001`

**Chạy toàn bộ VNA suite:**
- `TEST_SUITE = vna`
- `TEST_CASE = (để trống)`

**Dry-run không cần hardware:**
- `TEST_SUITE = demo`
- `SKIP_HW_TESTS = true`

**Chạy đúng commit đang sửa local:**
```cmd
git rev-parse --short HEAD
```
Điền SHA đó vào `GIT_COMMIT_ID`.

---

## 7. Xử lý lỗi thường gặp

### Lỗi: `No windows for that process could be found`

**Nguyên nhân:** Jenkins đang chạy trong Session 0 (service mode), không thể tạo GUI window.

**Fix:** Đảm bảo Jenkins chạy qua Task Scheduler với `/it` flag (xem mục 2), không chạy như service.

---

### Lỗi: `Could not create the process "C:\...\S2VNA.exe"`

**Nguyên nhân:** Đường dẫn exe sai hoặc app chưa được cài.

**Fix:** Kiểm tra `config/settings.yaml` và `Jenkinsfile` có đúng đường dẫn:
```yaml
s2vna:
  exe_path: "C:/VNA/S2VNA/S2VNA.exe"
```

---

### Lỗi: `Windows fatal exception: code 0x8001010d`

**Nguyên nhân:** COM threading conflict, thường xảy ra với Python 3.13+.

**Fix:** Đã được xử lý trong code bằng `comtypes.CoInitialize()` ở đầu `conftest.py` và `app_controller.py`. Nếu vẫn xảy ra, thử downgrade Python xuống 3.11.

---

### Lỗi: `pywinauto.timings.TimeoutError` tại `switch_window`

**Nguyên nhân:** Keyboard navigation `{DOWN}{DOWN}{DOWN}{ENTER}` không hoạt động vì window không có focus.

**Fix:** Đã xử lý trong `main_page.py` bằng `set_focus()` + `bring_to_top()` trước khi gửi phím. Nếu vẫn lỗi, tăng `NAV_WAIT` trong `MainPage`.

---

### Lỗi: `The service cannot be started (error 1058)`

**Nguyên nhân:** Jenkins service đã bị disabled.

**Fix:**
```cmd
sc config jenkins start= auto
net start jenkins
```
Hoặc dùng Task Scheduler thay vì service (khuyến nghị).

---

### Jenkins không load params mới sau khi sửa Jenkinsfile

**Fix:** Sau khi push Jenkinsfile mới, vào Jenkins → job → **Build with Parameters** → chạy 1 build bất kỳ. Lần sau sẽ thấy params mới.

---

## Cấu trúc thư mục Reports

Sau khi chạy xong, kết quả được lưu tại:

```
reports/
├── html/report.html        ← HTML report (xem trên Jenkins hoặc trình duyệt)
├── excel/test_results.xlsx ← Excel report với màu PASS/FAIL
├── junit.xml               ← JUnit XML (Jenkins đọc để hiển thị test trend)
├── logs/
│   ├── framework.log       ← Log của framework
│   └── pytest.log          ← Log đầy đủ của pytest
└── screenshots/            ← Screenshot tự động chụp khi test FAIL
```

Truy cập báo cáo trên Jenkins: **Job** → **Build** → **Test Report** (HTML) hoặc **Test Results** (JUnit).
