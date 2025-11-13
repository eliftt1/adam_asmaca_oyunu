import random
from datetime import datetime
import os
import json
from colorama import init, Fore, Style

# Colorama başlat (renkler için)
init(autoreset=True)

SCORES_FILE = "scores.json"
MAX_ERRORS = 6
FLOAT_TOL = 1e-6

# Adam asmaca görselleri
HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    ========""",
    """

     +---+
     |   |
     O   |
         |
         |
         |
    ========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    ========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    ========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    ========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    ========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    ========""",
]


def kategori_verisi():
    """Kelime ve kategorileri döndürür."""
    return {
        "meyveler": ["elma", "kiraz", "kayısı", "şeftali", "erik", "karadut", "muz", "çilek", "portakal", "karpuz", "armut", "kivi", "ananas", "mango", "üzüm", "ayva"],
        "sebzeler": ["domates", "patlıcan", "bamya", "enginar", "soğan", "salatalık", "havuç", "patates", "ıspanak", "biber", "kabak", "lahana", "brokoli", "pırasa"],
        "hayvanlar": ["kedi", "köpek", "papağan", "aslan", "tavuk", "leylek", "kaplan", "fil", "zebra", "ayı", "tavşan", "at", "maymun"],
        "teknoloji": ["bilgisayar", "monitör", "telefon", "yazılım", "robot", "algoritma", "sunucu", "kamera", "drone", "tablet", "modem"],
        "renkler": ["kırmızı", "mavi", "yeşil", "sarı", "turuncu", "mor", "pembe", "siyah", "beyaz", "gri", "kahverengi"],
        "ülkeler": ["türkiye", "almanya", "fransa", "italya", "ispanya", "amerika", "kanada", "brazil", "japonya", "çin", "rusya", "arjantin", "azerbaycan", "belçika"],
        "sporlar": ["futbol", "basketbol", "voleybol", "yüzme", "tenis", "güreş", "boks", "kayak", "hentbol", "badminton", "judo"],
    }


def rastegele_kelime_secimi(words_dict):
    """Kategorilerden rastgele kelime seçer."""
    kategori = random.choice(list(words_dict.keys()))
    kelime = random.choice(words_dict[kategori])
    return kategori, kelime.lower()


def oyun_ekrani(masked, guessed_letters, errors, bonus, kategori_known=False, kategori=None):
    """Oyun durumunu ekrana yazdırır."""
    print(Fore.CYAN + HANGMAN_STAGES[errors])
    print(Fore.WHITE + "\nKelime: ", " ".join(masked))
    print(Fore.MAGENTA + "Tahmin edilen harfler:", ", ".join(sorted(guessed_letters)) if guessed_letters else "Henüz Yok")
    print(Fore.YELLOW + f"Kalan hata hakkın: {MAX_ERRORS - errors} (Toplam hatalar: {errors})")
    print(Fore.GREEN + f"Bonus puanı: {bonus}")
    if kategori_known and kategori:
        print(Fore.BLUE + f"Kategori (ipucu ile): {kategori}")


def rastgele_harf_sec(kelime, masked):
    unopened = [i for i, ch in enumerate(masked) if ch == "_"]
    if not unopened:
        return None
    idx = random.choice(unopened)
    target = kelime[idx]
    for i, ch in enumerate(kelime):
        if ch == target and masked[i] == "_":
            masked[i] = target
    return target


def skor_kaydet(name, score):
    """scores.json'a kaydeder; en yüksek 5 skoru tutar."""
    entry = {"name": name, "score": score, "date": datetime.now().isoformat()}
    scores = []
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except Exception:
            scores = []
    scores.append(entry)
    scores = sorted(scores, key=lambda e: e["score"], reverse=True)[:5]
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


def skor_tablosu():
    """scores.json'daki en iyi 5 skoru gösterir."""
    if not os.path.exists(SCORES_FILE):
        print(Fore.YELLOW + "Henüz skor kaydı yok.")
        return
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            scores = json.load(f)
    except Exception:
        print(Fore.RED + "Skor dosyası okunamadı.")
        return
    if not scores:
        print(Fore.YELLOW + "Henüz skor kaydı yok.")
        return
    print(Fore.CYAN + "\n=== En Yüksek Skorlar ===")
    for i, s in enumerate(scores, 1):
        date = s.get("date", "")[:19].replace("T", " ")
        print(Fore.WHITE + f"{i}. {s.get('name','-')} — {s.get('score',0)} puan ({date})")
    print(Fore.CYAN + "\n=== En Yüksek Skorlar ===")


def sayi_al(prompt):
    """Kullanıcıdan sayı isteme yardımcı fonksiyonu."""
    while True:
        val = input(Fore.WHITE + prompt).strip()
        if val.lower() == "iptal":
            return None
        try:
            return float(val)
        except ValueError:
            print(Fore.RED + "Geçersiz sayı girdin. Tekrar dene ya da 'iptal' yaz.")


def matematik_oyunu(used_ops):
    ops_map = {"+": "toplama", "-": "çıkarma", "*": "çarpma", "/": "bölme"}
    available = [k for k in ops_map.keys() if k not in used_ops]
    if not available:
        print(Fore.RED + "Tüm işlemler zaten kullanıldı.")
        return ("error", "no_ops_left", None, None)

    print(Fore.CYAN + "Kullanılabilir işlemler:", ", ".join(f"{k} ({ops_map[k]})" for k in available))
    op = input(Fore.WHITE + "Bir işlem seçin (+ - * /) veya 'iptal' yazın: ").strip()
    if op.lower() == "iptal":
        return ("cancel", "user_cancel", None, None)
    if op not in ops_map:
        print(Fore.RED + "Geçersiz işlem seçimi.")
        return ("error", "invalid_op", None, None)
    if op in used_ops:
        print(Fore.RED + "Bu işlem zaten kullanıldı.")
        return ("error", "op_already_used", None, None)

    a = sayi_al("Birinci sayı (iptal için 'iptal'): ")
    if a is None:
        return ("cancel", "user_cancel", None, None)
    b = sayi_al("İkinci sayı (iptal için 'iptal'): ")
    if b is None:
        return ("cancel", "user_cancel", None, None)

    if op == "/" and abs(b) <= FLOAT_TOL:
        print(Fore.RED + "Bölen sıfır olamaz! Hata sayısı artacak.")
        return ("error", "divide_by_zero", op, False)

    expected = eval(f"{a}{op}{b}")

    result = sayi_al(f"Soru: {a} {op} {b} = ")
    if result is None:
        return ("cancel", "user_cancel", None, None)

    if abs(result - expected) <= FLOAT_TOL:
        print(Fore.GREEN + "✅ İşlem doğru!")
        return ("ok", "correct", op, True)
    else:
        print(Fore.RED + f"❌ Yanlış. Doğru sonuç: {expected}")
        return ("ok", "incorrect", op, False)


def play_game():
    words = kategori_verisi()
    kategori, kelime = rastegele_kelime_secimi(words)
    masked = ["_" for _ in kelime]
    guessed = set()
    errors = 0
    bonus = 0
    score = 0
    used_ops = set()
    kategori_revealed = False

    print(Fore.CYAN + "=== Calc & Hang — İşlem Yap, Harfi Kurtar ===")
    print(Fore.WHITE + "Kurallar: Bir harf tahmin et, işlem yaparak bonus kazan, ipucu al.")
    print(Fore.WHITE + "Not: İşlem sırasında 'iptal' yazarsan geri dönersin.")
    print(Fore.WHITE + "Oyundan çıkmak için 'q' yazabilirsiniz.\n")

    while errors < MAX_ERRORS and "_" in masked:
        oyun_ekrani(masked, guessed, errors, bonus, kategori_revealed, kategori if kategori_revealed else None)
        print(Fore.CYAN + "\nSeçenekler: (1) Harf tahmin et  (2) İşlem yap  (3) İpucu al  (4) Çıkış (q)")
        choice = input(Fore.WHITE + "Seçiminiz (1/2/3/q): ").strip().lower()

        if choice in ("q", "4"):
            print(Fore.YELLOW + "Oyundan çıkılıyor...")
            break

        if choice == "1":
            harf = input("Tahmin ettiğiniz harf: ").strip().lower()
            if len(harf) != 1 or not harf.isalpha():
                print(Fore.RED + "Lütfen sadece tek bir alfabetik karakter girin.")
                continue
            if harf in guessed:
                print(Fore.RED + "Bu harfi zaten tahmin ettiniz. Hata sayısı değişmez.")
                continue
            guessed.add(harf)
            if harf in kelime:
                for i, ch in enumerate(kelime):
                    if ch == harf:
                        masked[i] = harf
                print(Fore.GREEN + "✅ Doğru harf!")
                score += 10
            else:
                print(Fore.RED + "❌ Harf kelimede yok.")
                score -= 5
                errors += 1

        elif choice == "2":
            status, msg, op, correct = matematik_oyunu(used_ops)
            if status == "cancel":
                continue
            if status == "error" and msg == "divide_by_zero":
                errors += 1
                score -= 10
                used_ops.add(op)
                continue
            if status == "error":
                continue
            used_ops.add(op)
            if correct:
                score += 15
                bonus += 1
                opened = rastgele_harf_sec(kelime, masked)
                if opened:
                    print(Fore.YELLOW + f"Bir doğru harf otomatik açıldı: '{opened}'")
                else:
                    print(Fore.YELLOW + "Açılacak gizli harf kalmadı.")
            else:
                score -= 10
                errors += 1

        elif choice == "3":
            if bonus >= 1:
                bonus -= 1
                kategori_revealed = True
                print(Fore.BLUE + f"İpucu: Kelime kategorisi -> {kategori}")
            else:
                print(Fore.RED + "Yeterli bonusun yok. İpucu almak için 1 bonus gerekli.")
        else:
            print(Fore.RED + "Geçersiz seçim. Lütfen 1,2,3 veya q girin.")
            continue

        # 🔹 Son harf bulunduysa ekran güncellensin ve mesaj tek satırda gösterilsin
        if "_" not in masked:
            oyun_ekrani(masked, guessed, errors, bonus, kategori_revealed, kategori if kategori_revealed else None)
            print(Fore.GREEN + f"Tebrikler! Tüm harfleri buldunuz.")
            score += 50
            break

        if errors >= MAX_ERRORS:
            print(Fore.RED + "\nHata hakkınız doldu.")
            score -= 20
            break

    if "_" not in masked:
        print(Fore.GREEN + f"Kelime: {kelime}")
    else:
        if errors >= MAX_ERRORS:
            print(Fore.RED + f"Kaybettin maalesef! Doğru kelime '{kelime}' idi.")
        else:
            print(Fore.YELLOW + "Oyun çıkışı yapıldı. Son durum:")
            print(Fore.WHITE + "Kelime: ", " ".join(masked))

    print(Fore.CYAN + f"\nFinal Puanınız: {score} (Bonus kalan: {bonus})")
    save = input(Fore.WHITE + "Skorunuzu kaydetmek ister misiniz?  (e/h): ").strip().lower()
    if save in ("e", "evet", "y", "yes"):
        name = input(Fore.WHITE + "İsim girin (kullanıcı adı): ").strip()
        if not name:
            name = "misafir"
        skor_kaydet(name, score)
        print(Fore.GREEN + "Skor kaydedildi.")
    skor_tablosu()
    print(Fore.CYAN + "Oyun bitti. Umarım eğlenmişsindir :)")

if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n" + Fore.YELLOW + "Oyundan çıkıldı (CTRL+C). Görüşürüz!")