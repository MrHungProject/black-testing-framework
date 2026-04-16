
import time
from pywinauto import Application, Desktop
from pywinauto import mouse
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.03

APP_PATH = r"C:\PC17\PC17.exe"


# ================= HELPER =================
def click_text(root, text):
    for _ in range(5):
        for c in root.descendants():
            try:
                if c.window_text().strip().lower() == text.lower() and c.is_enabled():
                    print(f"🎯 Click TEXT: {text}")
                    c.click_input()
                    return True
            except:
                pass
        time.sleep(0.5)
    return False


def click_button(root, text):
    for _ in range(5):
        for c in root.descendants():
            try:
                if (
                    c.window_text().strip().lower() == text.lower()
                    and c.is_enabled()
                    and "Button" in str(c.element_info.control_type)
                ):
                    print(f"🎯 Click BUTTON: {text}")
                    c.click_input()
                    return True
            except:
                pass
        time.sleep(0.5)
    return False


def wait_until_connected(root, timeout=15):
    for _ in range(timeout):
        for c in root.descendants():
            try:
                if c.window_text().strip() == "Connected":
                    return True
            except:
                pass
        time.sleep(1)
    return False


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


def extract_detail(root):
    texts = get_texts(root)
    temp = None
    serial = None

    for i, t in enumerate(texts):
        if "Temperature" in t and i + 1 < len(texts):
            temp = texts[i + 1]
        if "Serial Number" in t and i + 1 < len(texts):
            serial = texts[i + 1]

    return temp, serial


# ================= VNA =================
def ensure_vna_open(main):
    for c in main.descendants():
        try:
            if c.window_text().strip() in ["Stimulus", "Measurement", "Markers"]:
                print("✅ VNA already OPEN")
                return
        except:
            pass

    print("👉 Opening VNA PANEL...")
    vna_panel = main.child_window(auto_id="CardCollapeVNA", control_type="Pane")
    vna_panel.wait("exists ready", timeout=10)
    vna_panel.click_input()
    time.sleep(1)


# ================= MEASUREMENT =================
def open_vna_measurement(main):
    print("\n👉 VNA → Measurement")
    ensure_vna_open(main)

    for _ in range(10):
        for c in main.descendants():
            try:
                if c.window_text().strip() == "Measurement":
                    c.click_input()
                    print("✅ Click Measurement")
                    time.sleep(2)
                    return
            except:
                pass
        time.sleep(1)

    raise Exception("❌ Cannot click Measurement")


def select_s_parameter(main, name):
    if not click_text(main, name):
        raise Exception(f"❌ Cannot select {name}")
    print(f"✅ Selected {name}")


def click_apply(main):
    if not click_text(main, "Apply"):
        raise Exception("❌ Cannot click Apply")
    print("✅ Applied")


# ================= STIMULUS =================
def open_vna_stimulus(main):
    print("\n👉 VNA → Stimulus")
    ensure_vna_open(main)

    for _ in range(5):
        for c in main.descendants():
            try:
                if c.window_text().strip() == "Stimulus":
                    c.click_input()
                    print("✅ Click Stimulus")
                    time.sleep(2)
                    return
            except:
                pass
        time.sleep(0.5)

    raise Exception("❌ Cannot click Stimulus")


def set_field_by_label(main, label, value):
    controls = list(main.descendants())

    for i, c in enumerate(controls):
        try:
            if c.window_text().strip() == label:
                for j in range(i + 1, i + 10):
                    try:
                        target = controls[j]

                        if "Edit" in str(target.element_info.control_type):
                            target.click_input()
                            time.sleep(0.2)

                            target.type_keys("^a{BACKSPACE}")
                            target.set_edit_text(str(value))
                            target.type_keys("{ENTER}")

                            print(f"✅ {label} = {value}")
                            return True
                    except:
                        pass
        except:
            pass

    raise Exception(f"❌ Cannot set field: {label}")


def set_stimulus_params(main):
    print("\n👉 Setting Stimulus")

    set_field_by_label(main, "Start Frequency", "2GHz")
    set_field_by_label(main, "Stop Frequency", "6GHz")
    set_field_by_label(main, "Center Frequency", "9.05GHz")
    set_field_by_label(main, "Span Frequency", "3GHz")
    set_field_by_label(main, "Number of Points", "301")
    set_field_by_label(main, "IF Bandwidth", "10kHz")
    set_field_by_label(main, "Power", "0")

    click_apply(main)
    print("✅ Stimulus DONE")


# ================= MARKER =================
def open_vna_markers(main):
    print("\n👉 VNA → Markers")
    ensure_vna_open(main)

    for _ in range(5):
        for c in main.descendants():
            try:
                if c.window_text().strip() == "Markers":
                    c.click_input()
                    print("✅ Click Markers")
                    time.sleep(1)
                    return
            except:
                pass
        time.sleep(1)

    raise Exception("❌ Cannot click Markers")


def click_add_marker(main):
    print("👉 Click Add Marker")

    if click_button(main, "Add Marker"):
        return

    if click_text(main, "Add Marker"):
        return

    raise Exception("❌ Cannot click Add Marker")

def open_trace_dropdown(main):
    print("👉 Open Trace dropdown")

    for _ in range(5):
        for c in main.descendants():
            try:
                if c.window_text().strip() == "Trace 1" and c.is_enabled():
                    print("🎯 Click Trace 1")
                    c.click_input()
                    time.sleep(1)
                    return True
            except:
                pass
        time.sleep(1)

    raise Exception("❌ Cannot open Trace dropdown")


def select_trace_from_popup(value="Trace 2"):
    print(f"👉 Select {value}")

    desktop = Desktop(backend="uia")

    for _ in range(5):
        for w in desktop.windows():
            try:
                texts = []

                for c in w.descendants():
                    try:
                        t = c.window_text().strip()
                        if t:
                            texts.append(t)
                    except:
                        pass

                if value in texts:
                    for c in w.descendants():
                        try:
                            if c.window_text().strip() == value and c.is_enabled():
                                print(f"🎯 Click {value}")
                                c.click_input()
                                time.sleep(1)
                                return True
                        except:
                            pass
            except:
                pass

        time.sleep(0.5)

    raise Exception(f"❌ Cannot select {value}")

def get_marker_panel(main):
    for c in main.descendants():
        try:
            if "Active Markers" in c.window_text():
                return c.parent()  # panel chứa marker
        except:
            pass
    return None

def extract_markers(main):
    panel = get_marker_panel(main)

    if not panel:
        raise Exception("❌ Cannot find marker panel")

    texts = []
    for c in panel.descendants():
        try:
            t = c.window_text().strip()
            if t:
                texts.append(t)
        except:
            pass

    markers = []
    current = None

    i = 0
    while i < len(texts):
        t = texts[i]

        # 👉 bắt đầu marker thật
        if t.startswith("Marker"):
            current = {"name": t, "position": None, "value": None}

            # scan trong phạm vi nhỏ phía sau
            for j in range(i + 1, min(i + 10, len(texts))):
                if texts[j] == "Position:" and j + 1 < len(texts):
                    current["position"] = texts[j + 1]

                if texts[j] == "Value:" and j + 1 < len(texts):
                    current["value"] = texts[j + 1]

            markers.append(current)

        i += 1

    return markers


def setup_marker(main):
    print("\n👉 Setup Marker")

    open_vna_markers(main)
    time.sleep(0.5)

    # ===== Marker 1 (Trace 1 default) =====
    click_add_marker(main)
    time.sleep(0.5)

    # ===== Đổi sang Trace 2 =====
    open_trace_dropdown(main)
    select_trace_from_popup("Trace 2")

    # ===== Marker 2 =====
    click_add_marker(main)

    print("🎉 Marker DONE (Trace1 + Trace2)")

def get_marker_texts(main):
    texts = []

    for c in main.descendants():
        try:
            t = c.window_text().strip()
            if t:
                texts.append(t)
        except:
            pass

    return texts

def extract_markers(main):
    # ===== 1. tìm đúng panel Active Markers =====
    panel = None
    for c in main.descendants():
        try:
            if "Active Markers" in c.window_text():
                panel = c.parent()
                break
        except:
            pass

    if not panel:
        raise Exception("❌ Cannot find Active Markers panel")

    # ===== 2. lấy text trong panel =====
    texts = []
    for c in panel.descendants():
        try:
            t = c.window_text().strip()
            if t:
                texts.append(t)
        except:
            pass

    # ===== 3. lọc giá trị thật =====
    values = []
    for t in texts:
        if "GHz" in t or "dB" in t:
            values.append(t)

    # DEBUG nếu cần
    # print("DEBUG:", values)

    # ===== 4. ghép thành marker =====
    markers = []
    i = 0

    while i < len(values) - 1:
        if "GHz" in values[i] and "dB" in values[i + 1]:
            markers.append({
                "name": f"Marker {len(markers)+1}",
                "position": values[i],
                "value": values[i + 1]
            })
            i += 2
        else:
            i += 1

    return markers


# ================= MAIN =================
print("🚀 Start app...")
app = Application(backend="uia").start(APP_PATH)
time.sleep(5)

dlg = app.top_window()

# Open RF Test Set
print("👉 Open RF Test Set")
dlg.child_window(title="Tools", control_type="MenuItem").click_input()
time.sleep(1)
dlg.type_keys("{DOWN}{DOWN}{DOWN}{ENTER}")
time.sleep(3)

main = app.window(title_re=".*FormMainEliteRF.*")
main.wait("visible", timeout=20)

# Connect
print("👉 Connect Device")
click_text(main, "System")
click_text(main, "Connect")
time.sleep(1)
click_text(main, "Connection")

if not wait_until_connected(main):
    raise Exception("❌ Not connected")

print("🎉 CONNECTED")

# Detail
click_text(main, "Detail")
time.sleep(1)

temp, serial = extract_detail(main)
print(f"Temp: {temp}")
print(f"Serial: {serial}")

if not temp or not serial:
    raise Exception("❌ Detail invalid")

print("🎉 DETAIL OK")

# Measurement
open_vna_measurement(main)
select_s_parameter(main, "S11")
select_s_parameter(main, "S21")
click_apply(main)

print("🎉 Measurement DONE")

# Stimulus
open_vna_stimulus(main)
set_stimulus_params(main)

# Marker
setup_marker(main)
markers = extract_markers(main)

for m in markers:
    print(m)

print("\n🚀 FULL TEST DONE SUCCESSFULLY")
