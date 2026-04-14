"""
tools/scan_ui.py — Scan UI elements của PC17 và S2VNA
======================================================

Chạy script này khi cả 2 app đang mở để lấy danh sách
tất cả các control (auto_id, title, class_name).

Dùng kết quả để điền vào pages/main_page.py và tests/vna/

Cách chạy (trên Windows, từ thư mục gốc project):
    python tools/scan_ui.py
    python tools/scan_ui.py --app S2VNA
    python tools/scan_ui.py --app PC17 --depth 8
    python tools/scan_ui.py --save   # lưu ra file txt
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from pywinauto import Application, Desktop
    from pywinauto.findwindows import find_windows
except ImportError:
    print("ERROR: pywinauto chưa được cài.")
    print("Chạy: pip install pywinauto")
    sys.exit(1)


def list_open_windows():
    """Liệt kê tất cả cửa sổ đang mở."""
    print("\n=== CÁC CỬA SỔ ĐANG MỞ ===")
    windows = Desktop(backend="uia").windows()
    for i, w in enumerate(windows):
        try:
            title = w.window_text()
            cls   = w.class_name()
            if title.strip():
                print(f"  [{i:2d}] title='{title}'  class='{cls}'")
        except Exception:
            pass
    print()


def scan_app(app_name: str, depth: int = 6, backend: str = "uia", save: bool = False):
    """Kết nối đến app đang chạy và in toàn bộ control tree."""
    print(f"\n=== SCANNING: '{app_name}' (backend={backend}) ===\n")
    try:
        app = Application(backend=backend).connect(title_re=f".*{app_name}.*", timeout=10)
    except Exception as e:
        print(f"Không tìm thấy '{app_name}': {e}")
        print(f"Hãy đảm bảo app đang mở và tên đúng.\n")
        return

    win = app.top_window()
    print(f"Window: '{win.window_text()}'\n")
    print("-" * 70)

    if save:
        out_path = Path(f"reports/scan_{app_name.replace(' ', '_')}.txt")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            win.print_control_identifiers(depth=depth)
        output = buf.getvalue()
        out_path.write_text(output, encoding="utf-8")
        print(output)
        print(f"\nĐã lưu ra: {out_path}")
    else:
        win.print_control_identifiers(depth=depth)

    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="Scan UI elements của Windows app")
    parser.add_argument("--app",    default=None,  help="Tên app (mặc định: scan cả 2)")
    parser.add_argument("--depth",  default=6, type=int, help="Độ sâu cây UI (default: 6)")
    parser.add_argument("--backend",default="uia", help="uia hoặc win32 (default: uia)")
    parser.add_argument("--save",   action="store_true", help="Lưu kết quả ra file txt")
    args = parser.parse_args()

    list_open_windows()

    if args.app:
        scan_app(args.app, depth=args.depth, backend=args.backend, save=args.save)
    else:
        # Scan cả 2 app mặc định
        for name in ["PC17", "S2VNA"]:
            scan_app(name, depth=args.depth, backend=args.backend, save=args.save)
            print()


if __name__ == "__main__":
    main()
