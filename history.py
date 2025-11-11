from datetime import datetime

class HistorySystem:
    def __init__(self, current_user=None):
        """
        current_user → dict, misal:
        {"username": "gamal", "role": "user"}
        """
        self.current_user = current_user
        self.data = {"history": []}  # bisa diganti load dari file JSON nanti

    def save_data(self):
        """Simulasi penyimpanan data ke file JSON"""
        # kalau kamu sudah pakai file JSON, tinggal ganti dengan save_json()
        pass

    def add_history(self, activity, details=""):
        """Menambah aktivitas ke history"""
        if not self.current_user:
            print("⚠️ Tidak ada user yang sedang login.")
            return
        
        history_entry = {
            "username": self.current_user["username"],
            "activity": activity,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": details
        }
        
        # Tambahkan ke list data history
        self.data["history"].append(history_entry)
        self.save_data()  # di versi lengkap, simpan ke file JSON

    def view_user_history(self):
        """Menampilkan history user yang sedang login"""
        if not self.current_user:
            print("⚠️ Tidak ada user yang sedang login.")
            return

        print("\n" + "=" * 50)
        print(f"           HISTORY - {self.current_user['username'].upper()}")
        print("=" * 50)
        
        # Filter history berdasarkan username aktif
        user_history = [h for h in self.data["history"] 
                        if h["username"] == self.current_user["username"]]
        
        if not user_history:
            print("Belum ada riwayat aktivitas.")
            return
        
        # Urutkan berdasarkan timestamp terbaru
        user_history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        print(f"Total aktivitas: {len(user_history)}")
        print("-" * 50)
        
        for i, entry in enumerate(user_history, 1):
            print(f"{i}. [{entry['timestamp']}]")
            print(f"   Aktivitas: {entry['activity']}")
            if entry["details"]:
                print(f"   Detail: {entry['details']}")
            print()

    def view_all_history(self):
        """Menampilkan semua history (admin only)"""
        if not self.current_user:
            print("⚠️ Tidak ada user yang sedang login.")
            return

        if self.current_user.get("role") != "admin":
            print("✗ Hanya admin yang dapat mengakses fitur ini!")
            return
        
        print("\n" + "=" * 50)
        print("           ALL HISTORY (ADMIN)")
        print("=" * 50)
        
        if not self.data["history"]:
            print("Belum ada riwayat aktivitas.")
            return
        
        # Urutkan berdasarkan timestamp terbaru
        all_history = sorted(self.data["history"], 
                             key=lambda x: x["timestamp"], reverse=True)
        
        print(f"Total aktivitas: {len(all_history)}")
        print("-" * 50)
        
        for i, entry in enumerate(all_history, 1):
            print(f"{i}. User: {entry['username']}")
            print(f"   Waktu: {entry['timestamp']}")
            print(f"   Aktivitas: {entry['activity']}")
            if entry["details"]:
                print(f"   Detail: {entry['details']}")
            print()
