import os, json

def load_soal(mapel):
    """Ambil soal dari file JSON tunggal"""
    try:
        with open("data/soal_saintek.json", "r", encoding="utf-8") as f:
            semua_soal = json.load(f)
            return semua_soal.get(mapel, [])
    except FileNotFoundError:
        print("❌ File soal_saintek.json tidak ditemukan.")
        return []

def jalankan_quiz(mapel, username, history_callback):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"=== QUIZ {mapel.upper()} ===")

    soal_list = load_soal(mapel)
    if not soal_list:
        print("Belum ada soal untuk mapel ini.")
        input("Tekan Enter untuk kembali...")
        return

    skor = 0
    for i, s in enumerate(soal_list, start=1):
        print(f"\nSoal {i}: {s['soal']}")
        for pilihan in s["pilihan"]:
            print(pilihan)
        jawaban = input("Jawaban kamu (A/B/C/D): ").upper().strip()
        if jawaban == s["jawaban"]:
            print("✅ Benar!")
            skor += 1
        else:
            print(f"❌ Salah! Jawaban benar: {s['jawaban']}")

    total = len(soal_list)
    persen = (skor / total) * 100
    print("\n=== HASIL AKHIR ===")
    print(f"Skor kamu: {skor}/{total}")
    print(f"Persentase: {persen:.1f}%")

    # Simpan ke history
    history_callback(f"Menyelesaikan Quiz {mapel}", f"Skor: {skor}/{total} ({persen:.1f}%)")
    input("\nTekan Enter untuk kembali ke menu utama...")
