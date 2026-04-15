from pywinauto import Application
import time

APP_PATH = r"C:\PC17\PC17.exe"

# ===== HELPER =====
def click_text(root, text):
    """Click control theo text"""
    for _ in range(5):
        for c in root.descendants():
            try:
                if c.window_text().strip().lower() == text.lower() and c.is_enabled():
                    c.click_input()
                    return True
            except:
                pass
        time.sleep(1)
    return False


def wait_until_connected(root, timeout=15):
    """Đợi trạng thái Connected"""
    for _ in range(timeout):
        for c in root.descendants():
            try:
                if c.window_text().strip() == "Connected":
                    return True
            except:
                pass
        time.sleep(1)
    return False


def has_disconnect(root):
    """Check có nút Disconnect"""
    for c in root.descendants():
        try:
            if c.window_text().strip() == "Disconnect" and c.is_enabled():
                return True
        except:
            pass
    return False


# ===== START APP =====
print("🚀 Start app...")
app = Application(backend="uia").start(APP_PATH)
time.sleep(5)

dlg = app.top_window()

# ===== Tools → RF Test Set =====
print("👉 Open RF Test Set")

dlg.child_window(title="Tools", control_type="MenuItem").click_input()
time.sleep(1)

# menu WinForms → keyboard fallback
dlg.type_keys("{DOWN}{DOWN}{DOWN}{ENTER}")
time.sleep(3)

# ===== WAIT MAIN WINDOW =====
main = app.window(title_re=".*FormMainEliteRF.*")
main.wait("visible", timeout=20)

print("✅ Opened:", main.window_text())
time.sleep(2)

# ===== CLICK SYSTEM =====
print("👉 Click System")

if not click_text(main, "System"):
    try:
        main.child_window(auto_id="CardSystem", control_type="Pane").click_input()
    except:
        print("❌ Không click được System")

time.sleep(1)

# ===== CLICK CONNECT =====
print("👉 Click Connect")

if not click_text(main, "Connect"):
    print("❌ Không click được Connect")

time.sleep(2)

# ===== CLICK CONNECTION =====
print("👉 Click Connection")

clicked = False

for _ in range(5):  # retry
    for c in main.descendants():
        try:
            if c.window_text().strip() == "Connection" and c.is_enabled():
                c.click_input()
                print("✅ Click Connection")
                clicked = True
                break
        except:
            pass

    if clicked:
        break

    time.sleep(1)

if not clicked:
    print("❌ Không click được Connection")
    input("Press Enter to exit...")
    exit()

# ===== VERIFY CONNECTION =====
# ===== VERIFY CONNECTION =====
print("⏳ Waiting for CONNECTED status...")

connected = wait_until_connected(main)
disconnect_btn = has_disconnect(main)

print("\n===== RESULT =====")

# ===== ASSERT LOGIC =====
if connected and disconnect_btn:
    print("🎉 TEST PASS - Device CONNECTED")
else:
    print("💥 TEST FAILED - Device NOT connected")

    # debug thêm
    if not connected:
        print("❌ Không thấy trạng thái 'Connected'")

    if not disconnect_btn:
        print("❌ Không thấy nút 'Disconnect'")

    # dừng chương trình (chuẩn automation)
    raise Exception("TEST FAILED: Connection không thành công")
# ===== CLICK DETAIL =====
print("\n👉 Click Detail")

if not click_text(main, "Detail"):
    print("❌ Không click được Detail")
    raise Exception("FAIL: Cannot open Detail panel")

time.sleep(2)

# ===== LẤY TEXT =====
def get_texts(root):
    texts = []
    for c in root.descendants():
        try:
            t = c.window_text().strip()
            if t:
                texts.append(t)
        except:
            pass
    return texts


texts = get_texts(main)

# ===== EXTRACT DATA (FIX CHUẨN) =====
temperature_value = None
serial_value = None

texts = get_texts(main)

for i, t in enumerate(texts):
    # ===== TEMPERATURE =====
    if "Temperature" in t:
        # lấy text ngay sau nó
        if i + 1 < len(texts):
            temperature_value = texts[i + 1]

    # ===== SERIAL NUMBER =====
    if "Serial Number" in t:
        if i + 1 < len(texts):
            serial_value = texts[i + 1]

# ===== PRINT RESULT =====
print("\n===== DETAIL DATA =====")

print(f"🌡 Temperature: {temperature_value}")
print(f"🔢 Serial Number: {serial_value}")

# ===== VALIDATION =====
temp_ok = temperature_value not in [None, "", ":"]
serial_ok = serial_value not in [None, "", ":"]

print("\n===== VALIDATION =====")

print(f"Temperature valid: {'✅' if temp_ok else '❌'}")
print(f"Serial valid: {'✅' if serial_ok else '❌'}")

# ===== FINAL RESULT =====
if temp_ok and serial_ok:
    print("\n🎉 DETAIL CHECK PASS")
else:
    print("\n💥 DETAIL CHECK FAIL")
    raise Exception("FAIL: Detail data invalid")