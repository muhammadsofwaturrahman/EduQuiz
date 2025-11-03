import json
import random
import os
import argparse

# File untuk menyimpan data
QUESTIONS_FILE = 'questions.json'
PROGRESS_FILE = 'progress.json'

# Fungsi untuk memuat data dari file
def load_data(filename, default_data):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return default_data

# Fungsi untuk menyimpan data ke file
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Inisialisasi data default
questions = load_data(QUESTIONS_FILE, {
    "matematika": [
        {"question": "Berapa 2 + 2?", "options": ["3", "4", "5"], "answer": "4"},
        {"question": "Berapa akar kuadrat dari 16?", "options": ["3", "4", "5"], "answer": "4"}
    ],
    "sejarah": [
        {"question": "Tahun berapa Indonesia merdeka?", "options": ["1945", "1946", "1947"], "answer": "1945"}
    ]
})
progress = load_data(PROGRESS_FILE, {"scores": [], "history": []})

# Fitur 1: Quiz Interaktif
def quiz_interactive():
    print("\n=== Quiz Interaktif ===")
    topics = list(questions.keys())
    if not topics:
        print("Tidak ada topik tersedia. Tambahkan via Mode Guru.")
        return
    print("Topik tersedia:", ", ".join(topics))
    topic = input("Pilih topik: ").strip().lower()
    if topic not in questions:
        print("Topik tidak ditemukan.")
        return
    
    score = 0
    total = len(questions[topic])
    for q in questions[topic]:
        print(f"\nPertanyaan: {q['question']}")
        for i, opt in enumerate(q['options'], 1):
            print(f"{i}. {opt}")
        try:
            answer = int(input("Jawaban (nomor): ")) - 1
            if q['options'][answer] == q['answer']:
                print("Benar!")
                score += 1
            else:
                print(f"Salah! Jawaban benar: {q['answer']}")
        except (ValueError, IndexError):
            print("Input tidak valid.")
    
    percentage = (score / total) * 100 if total > 0 else 0
    print(f"Skor Anda: {score}/{total} ({percentage:.2f}%)")
    progress["scores"].append({"topic": topic, "score": score, "total": total, "percentage": percentage})
    save_data(PROGRESS_FILE, progress)

# Fitur 2: Simulasi Matematika
def math_simulation():
    print("\n=== Simulasi Matematika ===")
    operations = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}
    level = input("Pilih level (easy/medium/hard): ").strip().lower()
    ranges = {"easy": (1, 10), "medium": (10, 50), "hard": (50, 100)}
    if level not in ranges:
        print("Level tidak valid.")
        return
    
    min_val, max_val = ranges[level]
    score = 0
    for _ in range(5):  # 5 soal
        a, b = random.randint(min_val, max_val), random.randint(min_val, max_val)
        op = random.choice(list(operations.keys()))
        correct = operations[op](a, b)
        print(f"Berapa {a} {op} {b}?")
        try:
            answer = int(input("Jawaban: "))
            if answer == correct:
                print("Benar!")
                score += 1
            else:
                print(f"Salah! Jawaban benar: {correct}")
        except ValueError:
            print("Input harus angka.")
    
    percentage = (score / 5) * 100
    print(f"Skor: {score}/5 ({percentage:.2f}%)")
    progress["history"].append({"type": "math_sim", "level": level, "score": score, "total": 5})
    save_data(PROGRESS_FILE, progress)

# Fitur 3: Pelacakan Kemajuan
def track_progress():
    print("\n=== Pelacakan Kemajuan ===")
    if not progress["scores"]:
        print("Belum ada skor quiz.")
        return
    total_quiz = len(progress["scores"])
    avg_percentage = sum(s["percentage"] for s in progress["scores"]) / total_quiz
    print(f"Total Quiz: {total_quiz}")
    print(f"Rata-rata Persentase: {avg_percentage:.2f}%")
    print("Riwayat Skor Terbaru:")
    for s in progress["scores"][-5:]:  # Tampilkan 5 terakhir
        print(f"- {s['topic']}: {s['score']}/{s['total']} ({s['percentage']:.2f}%)")
    
    if progress["history"]:
        math_sessions = [h for h in progress["history"] if h["type"] == "math_sim"]
        if math_sessions:
            avg_math = sum(h["score"] / h["total"] * 100 for h in math_sessions) / len(math_sessions)
            print(f"Rata-rata Simulasi Matematika: {avg_math:.2f}%")

# Fitur 4: Mode Guru (Tambah Pertanyaan)
def guru_mode():
    print("\n=== Mode Guru ===")
    topic = input("Topik baru atau yang ada: ").strip().lower()
    question = input("Pertanyaan: ").strip()
    options = [input(f"Opsi {i+1}: ").strip() for i in range(3)]
    answer = input("Jawaban benar (teks): ").strip()
    if answer not in options:
        print("Jawaban harus salah satu opsi.")
        return
    if topic not in questions:
        questions[topic] = []
    questions[topic].append({"question": question, "options": options, "answer": answer})
    save_data(QUESTIONS_FILE, questions)
    print("Pertanyaan ditambahkan!")

# Menu Utama CLI
def main():
    parser = argparse.ArgumentParser(description="EduQuiz CLI - Platform Pembelajaran Interaktif")
    parser.add_argument("--menu", choices=["quiz", "math", "progress", "guru"], help="Pilih fitur langsung")
    args = parser.parse_args()
    
    if args.menu:
        if args.menu == "quiz":
            quiz_interactive()
        elif args.menu == "math":
            math_simulation()
        elif args.menu == "progress":
            track_progress()
        elif args.menu == "guru":
            guru_mode()
        return
    
    while True:
        print("\n=== EduQuiz CLI ===")
        print("1. Quiz Interaktif")
        print("2. Simulasi Matematika")
        print("3. Pelacakan Kemajuan")
        print("4. Mode Guru")
        print("5. Keluar")
        choice = input("Pilih menu: ").strip()
        if choice == "1":
            quiz_interactive()
        elif choice == "2":
            math_simulation()
        elif choice == "3":
            track_progress()
        elif choice == "4":
            guru_mode()
        elif choice == "5":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
