import sys
import subprocess
import os
import platform
import time
import shutil

# ───────────────────────────────────────────────
# 📦 Tự cài module nếu cần
def install_and_import(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"[📦] Chưa có module '{module_name}', đang cài đặt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"[✅] Đã cài '{module_name}'.")

required_modules = ["os", "platform", "subprocess", "time", "shutil"]
for module in required_modules:
    install_and_import(module)

# ───────────────────────────────────────────────
# 🔄 Clear màn hình
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# ───────────────────────────────────────────────
# 🎨 Banner
def print_banner():
    clear_screen()
    banner = r"""
   ____                      _                              
  |  _ \ ___  ___ _ __   ___| |_ _ __ ___  _ __   ___ _ __  
  | |_) / _ \/ __| '_ \ / _ \ __| '__/ _ \| '_ \ / _ \ '__| 
  |  __/ (_) \__ \ |_) |  __/ |_| | | (_) | | | |  __/ |    
  |_|   \___/|___/ .__/ \___|\__|_|  \___/|_| |_|\___|_|    
                 |_|      🔥 App Launcher v1.0 🔥        
    """
    print(banner)
    print("=" * 60 + "\n")

# ───────────────────────────────────────────────
# 🪟 Windows Activation
def check_windows_activation():
    try:
        result = subprocess.run(["slmgr", "/xpr"], capture_output=True, text=True)
        output = result.stdout + result.stderr
        if "permanently activated" in output.lower():
            return True
        else:
            return False
    except Exception:
        print("Error checking windows")
        return None

def activate_windows():
    print("[🔧] Đang kích hoạt Windows...")
    try:
        commands = [
            'slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX',
            'slmgr /skms kms.digiboy.ir',
            'slmgr /ato'
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True)
        print("[✅] Kích hoạt xong! Khởi động lại sẽ có hiệu lực.")
    except Exception:
        print("Error activating windows")

# ───────────────────────────────────────────────
# ⚙️ Startup
def get_startup_path():
    return os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")

def is_in_startup():
    shortcut_path = os.path.join(get_startup_path(), "AutoGameLauncher.bat")
    return os.path.exists(shortcut_path)

def add_to_startup():
    startup_folder = get_startup_path()
    current_script = os.path.realpath(__file__)
    shortcut_path = os.path.join(startup_folder, "AutoGameLauncher.bat")
    with open(shortcut_path, "w") as f:
        f.write(f'start "" python "{current_script}"\n')
    print("[✅] Đã thêm vào khởi động cùng Windows.")

# 👉 Menu hỏi người dùng có muốn thêm vào startup (chỉ hỏi nếu chưa có)
def startup_menu():
    if is_in_startup():
        print("🟢 Đã nằm trong khởi động cùng Windows.")
        time.sleep(1.5)
        return

    print("⚙️  Bạn có muốn thêm chương trình vào khởi động cùng Windows không?")
    print("1. ✅ Có")
    print("2. ❌ Không")

    choice = input("\n🔘 Nhập lựa chọn: ")
    if choice == "1":
        add_to_startup()
        time.sleep(1.5)
    elif choice == "2":
        print("➡️ Không thêm vào khởi động.")
        time.sleep(1.5)
    else:
        print("❌ Lựa chọn không hợp lệ, bỏ qua.")
        time.sleep(1.5)

# ───────────────────────────────────────────────
# 🕹️ Game
apps = {
    "F04": r"C:\Program Files\F04\F04.exe",
    "LOL": r"C:\Riot Games\League of Legends\LeagueClient.exe"
}

def open_app(path, name):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        print(f"[✅] Đã mở {name}")
    except Exception as e:
        print(f"[❌] Không thể mở {name}: {e}")

def game_menu():
    while True:
        clear_screen()
        print("🎮 Danh sách trò chơi:")
        for i, name in enumerate(apps.keys(), start=1):
            print(f"{i}. {name}")
        print("0. Thoát")

        choice = input("\n🔘 Nhập số để mở game: ")
        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(apps):
            name = list(apps.keys())[int(choice) - 1]
            print(f"\n🔄 Đang mở {name}...")
            open_app(apps[name], name)
            time.sleep(2)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            time.sleep(1.5)

# ───────────────────────────────────────────────
# ▶️ MAIN
if __name__ == "__main__":
    print_banner()

    if platform.system() != "Windows":
        print("[❌] Hệ điều hành không phải Windows, thoát.")
        exit()

    print("[ℹ️] Kiểm tra trạng thái Windows...")
    status = check_windows_activation()
    if status is False:
        activate_windows()
    elif status is True:
        print("Windows already active!!!")
    elif status is None:
        pass

    time.sleep(1.5)
    clear_screen()

    startup_menu()
    clear_screen()

    game_menu()
