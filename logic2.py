from deep_translator import GoogleTranslator
from collections import defaultdict

questions = {
    'siapa namamu' : "Saya adalah bot super keren dan tujuan saya adalah untuk membantu Anda!",
    "berapa usiamu" : "Itu terlalu filosofis..."
}

class TextAnalysis():
    
    memory = defaultdict(list)

    def __init__(self, text, owner):
        TextAnalysis.memory[owner].append(self)

        self.text = text
        # Menerjemahkan dari Bahasa Indonesia ('id') ke Bahasa Inggris ('en')
        self.translation = self.__translate(self.text, "id", "en")

        if self.text in questions.keys():
            self.response = questions[self.text]
        else:
            self.response = self.get_answer() 

    def get_answer(self):
        return "Saya tidak tahu bagaimana membantu"

    def __translate(self, text, from_lang="id", to_lang="en"):
        try:
            # Memastikan teks tidak kosong sebelum dikirim ke API
            if not text or not text.strip():
                return "Teks kosong"
                
            # Menggunakan GoogleTranslator dari pustaka deep-translator
            translation = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
            return translation
        except Exception as e:
            print(f"Eror Penerjemah: {e}")
            return "Terjemahan gagal"