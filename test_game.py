import unittest
import os
import json
import game  # Ana oyun dosyanızı 'game.py' olarak import ediyoruz

class TestCalcAndHang(unittest.TestCase):

    # Testlerin her birinden önce çalışan hazırlık fonksiyonu
    def setUp(self):
        """Testler için geçici bir skor dosyası ayarla."""
        # Testlerin ana 'scores.json' dosyasını bozmaması için
        # game modülündeki SCORES_FILE değişkenini geçici olarak değiştiriyoruz.
        self.test_scores_file = "test_scores.json"
        game.SCORES_FILE = self.test_scores_file
        
        # Eğer önceki testten kalma bir dosya varsa sil
        if os.path.exists(self.test_scores_file):
            os.remove(self.test_scores_file)

    # Testlerin her birinden sonra çalışan temizlik fonksiyonu
    def tearDown(self):
        """Geçici skor dosyasını temizle."""
        if os.path.exists(self.test_scores_file):
            os.remove(self.test_scores_file)

    def test_kategori_verisi(self):
        """
        Bileşen: kategori_verisi()
        Test: Fonksiyonun bir sözlük (dict) döndürdüğünü ve içinin boş olmadığını doğrular.
        """
        data = game.kategori_verisi()
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        # Örnek bir anahtarın varlığını kontrol et
        self.assertIn("meyveler", data)
        self.assertIsInstance(data["meyveler"], list)

    def test_rastegele_kelime_secimi(self):
        """
        Bileşen: rastegele_kelime_secimi()
        Test: Fonksiyonun, kaynak veride bulunan geçerli bir (kategori, kelime) 
              ikilisi döndürdüğünü doğrular.
        """
        words_dict = game.kategori_verisi()
        kategori, kelime = game.rastegele_kelime_secimi(words_dict)
        
        self.assertIn(kategori, words_dict)
        self.assertIn(kelime, words_dict[kategori])
        self.assertEqual(kelime, kelime.lower()) # Kelimenin küçük harf olduğunu doğrula

    def test_rastgele_harf_sec(self):
        """
        Bileşen: rastgele_harf_sec()
        Test: Harf açma mantığını test eder.
        """
        # Senaryo 1: Tek bir harfi açma
        kelime = "elma"
        masked = ["_", "l", "m", "_"]
        opened = game.rastgele_harf_sec(kelime, masked)
        
        # 'e' veya 'a' harfini açmalı
        self.assertIn(opened, ['e', 'a'])
        # Maskelenmiş listeyi doğru güncelledi mi?
        if opened == 'e':
            self.assertEqual(masked, ["e", "l", "m", "_"])
        else: # opened == 'a'
            self.assertEqual(masked, ["_", "l", "m", "a"])

        # Senaryo 2: Birden fazla aynı harfi açma
        kelime = "ananas"
        masked = ["_", "n", "_", "n", "_", "s"]
        opened = game.rastgele_harf_sec(kelime, masked) # 'a' harfini açmalı
        
        self.assertEqual(opened, 'a')
        # Tüm 'a' harfleri açıldı mı?
        self.assertEqual(masked, ["a", "n", "a", "n", "a", "s"])

        # Senaryo 3: Tüm harfler zaten açıksa
        kelime = "kedi"
        masked = ["k", "e", "d", "i"]
        opened = game.rastgele_harf_sec(kelime, masked)
        self.assertIsNone(opened) # Hiçbir şey açmamalı (None döndürmeli)

    # test_game.py dosyanızda SADECE bu fonksiyonu güncelleyin

    def test_skor_kaydet(self):
        """
        Bileşen: skor_kaydet()
        Test: Skorların dosyaya doğru yazıldığını, sıralandığını ve 
              5 ile limitlendiğini doğrular.
        """
        # 6 farklı skor ekleyelim (limit 5)
        game.skor_kaydet("Ali", 100)
        game.skor_kaydet("Veli", 300)
        game.skor_kaydet("Ayşe", 50)     # Bu skorun liste dışı kalması beklenir
        game.skor_kaydet("Fatma", 200)
        game.skor_kaydet("Zeki", 400)
        game.skor_kaydet("Mert", 250)     # Bu skor 3. sıraya girmeli

        # Dosya oluşturuldu mu?
        self.assertTrue(os.path.exists(self.test_scores_file))

        # Dosyayı oku ve doğrula
        with open(self.test_scores_file, "r", encoding="utf-8") as f:
            scores = json.load(f)
        
        # 1. Test: Sadece 5 skor mu tutuluyor?
        self.assertEqual(len(scores), 5)
        
        # 2. Test: Skorlar doğru sıralanmış mı? (En yüksek en üstte)
        self.assertEqual(scores[0]["name"], "Zeki")  # 1. sıra (400 puan)
        self.assertEqual(scores[1]["name"], "Veli")  # 2. sıra (300 puan)
        
        # 3. Test: DÜZELTİLMİŞ KONTROLLER
        # Hata buradaydı. Mert 3. sırada (index 2), Ali 5. sırada (index 4) olmalı.
        self.assertEqual(scores[2]["name"], "Mert")  # 3. sıra (250 puan)
        self.assertEqual(scores[3]["name"], "Fatma") # 4. sıra (200 puan)
        self.assertEqual(scores[4]["name"], "Ali")   # 5. sıra (100 puan)

# Bu satır, dosyanın doğrudan çalıştırıldığında testleri başlatmasını sağlar
if __name__ == '__main__':
    unittest.main()