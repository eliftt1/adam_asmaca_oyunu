import unittest
import os
import json
import game 

class TestCalcAndHang(unittest.TestCase):

    # Testlerin her birinden önce çalışan hazırlık fonksiyonu
    def setUp(self):
        self.test_scores_file = "test_scores.json"
        game.SCORES_FILE = self.test_scores_file
        
        if os.path.exists(self.test_scores_file):
            os.remove(self.test_scores_file)

    def tearDown(self):
        if os.path.exists(self.test_scores_file):
            os.remove(self.test_scores_file)

    def test_kategori_verisi(self):
        data = game.kategori_verisi()
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        self.assertIn("meyveler", data)
        self.assertIsInstance(data["meyveler"], list)

    def test_rastegele_kelime_secimi(self):
        words_dict = game.kategori_verisi()
        kategori, kelime = game.rastegele_kelime_secimi(words_dict)
        self.assertIn(kategori, words_dict)
        self.assertIn(kelime, words_dict[kategori])
        self.assertEqual(kelime, kelime.lower()) 

    def test_rastgele_harf_sec(self):
        kelime = "elma"
        masked = ["_", "l", "m", "_"]
        opened = game.rastgele_harf_sec(kelime, masked)
        
        self.assertIn(opened, ['e', 'a'])
        if opened == 'e':
            self.assertEqual(masked, ["e", "l", "m", "_"])
        else:
            self.assertEqual(masked, ["_", "l", "m", "a"])

        # Birden fazla aynı harfi açma
        kelime = "ananas"
        masked = ["_", "n", "_", "n", "_", "s"]
        opened = game.rastgele_harf_sec(kelime, masked) 
        
        self.assertEqual(opened, 'a')
        self.assertEqual(masked, ["a", "n", "a", "n", "a", "s"])

        # Tüm harfler zaten açıksa 
        kelime = "kedi"
        masked = ["k", "e", "d", "i"]
        opened = game.rastgele_harf_sec(kelime, masked)
        self.assertIsNone(opened)

    def test_skor_kaydet(self):
        game.skor_kaydet("Ali", 100)
        game.skor_kaydet("Veli", 300)
        game.skor_kaydet("Ayşe", 50)    
        game.skor_kaydet("Fatma", 200)
        game.skor_kaydet("Zeki", 400)
        game.skor_kaydet("Mert", 250)   

        self.assertTrue(os.path.exists(self.test_scores_file))

        with open(self.test_scores_file, "r", encoding="utf-8") as f:
            scores = json.load(f)
            
        self.assertEqual(len(scores), 5)
        
        # Skorlar doğru sıralanmış mı? 
        self.assertEqual(scores[0]["name"], "Zeki")  
        self.assertEqual(scores[1]["name"], "Veli")  
        self.assertEqual(scores[2]["name"], "Mert") 
        self.assertEqual(scores[3]["name"], "Fatma") 
        self.assertEqual(scores[4]["name"], "Ali")  

# Bu satır, dosyanın doğrudan çalıştırıldığında testleri başlatmasını sağlar
if __name__ == '__main__':
    unittest.main()
