import json, os, time
from datetime import datetime
from colorama import Fore, Style, init
from quiz_saintek import jalankan_quiz

init(autoreset=True)

# ---------------- UTILITAS JSON ----------------
def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------------- ANIMASI DAN UI ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def print_banner(title):
    clear()
    border = "=" * 50
    print(Fore.CYAN + border)
    print(Fore.YELLOW + title.center(50))
    print(Fore.CYAN + border)

# ---------------- SISTEM LOGIN ----------------
def load_users():
    return load_json("data/users.json")

def save_users(users):
    save_json("data/users.json", users)

def register():
    print_banner("🔐 REGISTER AKUN BARU 🔐")
    users = load_users()
    username = input(Fore.GREEN + "Masukkan username baru: " + Fore.RESET)
    if any(u["username"] == username for u in users):
        print(Fore.RED + "❌ Username sudah digunakan.")
        input("Tekan Enter untuk kembali...")
        return None
    password = input(Fore.GREEN + "Masukkan password: " + Fore.RESET)
    users.append({"username": username, "password": password})
    save_users(users)
    print(Fore.GREEN + "✅ Akun berhasil dibuat! Selamat datang, " + username)
    time.sleep(1)
    return username

def login():
    print_banner("🔑 LOGIN QUIZ SAINTEK 🔑")
    users = load_users()
    username = input(Fore.CYAN + "Masukkan username: " + Fore.RESET)
    password = input(Fore.CYAN + "Masukkan password: " + Fore.RESET)

    print(Fore.YELLOW + "\nMemeriksa akun", end="")
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print("\n")

    for u in users:
        if u["username"] == username and u["password"] == password:
            print(Fore.GREEN + f"✅ Login berhasil! Selamat datang, {username} 👋")
            time.sleep(1)
            return username

    print(Fore.RED + "❌ Username atau password salah.")
    input("Tekan Enter untuk kembali...")
    return None

# ---------------- SISTEM HISTORY ----------------
def add_history(username, activity, details=""):
    history_file = "data/history.json"
    history = load_json(history_file)
    history.append({
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "activity": activity,
        "details": details
    })
    save_json(history_file, history)

def show_history(username):
    clear()
    print(Fore.CYAN + f"=== HISTORY - {username.upper()} ===")
    history = load_json("data/history.json")
    user_history = [h for h in history if h["username"] == username]
    if not user_history:
        print(Fore.RED + "Belum ada riwayat aktivitas.")
    else:
        user_history.sort(key=lambda x: x["timestamp"], reverse=True)
        for h in user_history[-10:]:
            print(f"{Fore.YELLOW}[{h['timestamp']}] {Fore.WHITE}{h['activity']} ({h['details']})")
    input("\nTekan Enter untuk kembali...")

# ---------------- MENU UTAMA ----------------
def menu_utama(username):
    while True:
        clear()
        print(Fore.CYAN + "=" * 50)
        print(Fore.YELLOW + f"MENU UTAMA - USER: {username}".center(50))
        print(Fore.CYAN + "=" * 50)
        print(Fore.GREEN + "1. Quiz Saintek")
        print("2. History")
        print("0. Logout")
        print(Fore.CYAN + "-" * 50)
        pilihan = input(Fore.WHITE + "Pilih menu: ")

        if pilihan == "1":
            try:
                with open("data/soal_saintek.json", "r", encoding="utf-8") as f:
                    semua_soal = json.load(f)
                    mapel_list = list(semua_soal.keys())
            except FileNotFoundError:
                print(Fore.RED + "❌ File soal_saintek.json tidak ditemukan!")
                input("Tekan Enter untuk lanjut...")
                continue

            print_banner("📚 PILIH MATA PELAJARAN 📚")
            for i, m in enumerate(mapel_list, 1):
                print(Fore.YELLOW + f"{i}. {m}")
            print(Fore.RED + "0. Kembali")
            pilih = input("\nPilih: ").strip()

            if pilih == "0":
                continue
            if pilih.isdigit() and 1 <= int(pilih) <= len(mapel_list):
                mapel = mapel_list[int(pilih)-1]
                jalankan_quiz(mapel, username, lambda a,d: add_history(username,a,d))
            else:
                print(Fore.RED + "Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")
        elif pilihan == "2":
            show_history(username)
        elif pilihan == "0":
            break

# ---------------- MAIN PROGRAM ----------------
def main():
    print_banner("🎓 SELAMAT DATANG DI QUIZ SAINTEK CLI 🎓")
    while True:
        print(Fore.GREEN + "1. Login")
        print("2. Register")
        print(Fore.RED + "0. Keluar")
        print(Fore.CYAN + "-" * 50)
        pilihan = input(Fore.WHITE + "Pilih menu: ")

        if pilihan == "1":
            username = login()
            if username:
                menu_utama(username)
        elif pilihan == "2":
            username = register()
            if username:
                menu_utama(username)
        elif pilihan == "0":
            print(Fore.YELLOW + "👋 Terima kasih telah bermain!")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    main()
